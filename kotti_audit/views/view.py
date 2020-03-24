# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import json
from pyramid.view import view_config
from pyramid.view import view_defaults
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from kotti_audit import _
from kotti_audit import utils
from kotti_audit.fanstatic import css_and_js
from kotti_audit.views import BaseView
from kotti.resources import Content


@view_defaults(permission='edit', context=Content)
class AuditLogViews(BaseView):
    """ Views for :class:`kotti_audit.resources.CustomContent` """

    @view_config(name='audit-log', permission='view',
                 renderer='kotti_audit:templates/audit-log.pt')
    def default_view(self):
        """ Default view`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """
        css_and_js.need()
        
        content_types = Content.query.distinct(
            Content.type).with_entities(Content.type).all();

        return {
            'type_filters': json.dumps(
                {t.type: t.type.title() for t in content_types})
        }

    @view_config(name="audit-api", permission="admin",
                 renderer="json")
    def audit_api(self):
        """ API view`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """
        limit = int(self.request.params.get("limit", 50))
        offset = int(self.request.params.get("offset", 0))
        sort = self.request.params.get("sort", "modification_date")
        order = self.request.params.get("order", "desc")
        filters = self.request.params.get("filter", None)
        search = self.request.params.get("search", None)

        query = Content.query;

        # Use the current context as the base location of the search,
        # otherwise, use root as the base location if no parent is found.
        parent_id = self.context.id if self.context.__parent__ else 0
        if parent_id != 0:
            query = query.filter(
                Content.path.ilike('{}%'.format(self.context.path)),
                Content.id != self.context.id
            )

        if filters is not None:
            filters = json.loads(filters)
        
            if 'creation_date' in filters:
                creation_date = filters['creation_date']
                query = utils.date_query(query, 'creation_date', creation_date)
        
            if 'modification_date' in filters:
                modification_date = filters['modification_date']
                query = utils.date_query(query, 'modification_date', modification_date)
            
            if 'title' in filters:
                query = query.filter(
                    Content.title.ilike("%{}%".format(filters['title'])))
            
            if 'type' in filters:
                query = query.filter_by(type=filters['type'].lower())
            
            if 'parent' in filters:
                parent_title = filters['parent']
                
                parent_ids = Content.query.filter(
                    Content.title.ilike("%{}%".format(parent_title))
                ).values('id')
                
                query = query.filter(
                    Content.parent_id.in_([r[0] for r in parent_ids])
                )


        if search:
            
            # Remvoe the current filters' value from the search text.
            if filters:
                for v in filters.values():
                    search = search.replace(v, '')
            search = search.strip()
            query = query.filter(
                Content.title.ilike("%{}%".format(search))
            )

        if order == 'asc':
            query = query.order_by(Content.__dict__.get(sort).asc())
        else:
            query = query.order_by(Content.__dict__.get(sort).desc())

        total_query = query.count()
        if offset > 0:
            query = query.offset(offset)
        if limit > 0:
            query = query.limit(limit)

        # import pdb; pdb.set_trace()
        # build bootstrap table response.
        query_json = [
            {
                "title": f.title,
                "parent": f.parent.title if f.parent is not None else '',
                "path": f.path,
                'type': f.type.title(),
                "url": f.path,
                "id": f.id,
                "creation_date": f.creation_date.strftime(
                    "%A %d. %B %Y - %I:%M%p %z ") or '',
                "modification_date": f.modification_date.strftime(
                    "%A %d. %B %Y - %I:%M%p %z ") or ''
            }
            for f in query
        ]
        return {
            "rows": query_json,
            "total": total_query
        }

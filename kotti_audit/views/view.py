# -*- coding: utf-8 -*-

"""
Created on 2020-03-21
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_audit import _
from kotti_audit.fanstatic import css_and_js
from kotti_audit.views import BaseView
from kotti.resources import Content


@view_defaults(permission='edit', context=Content)
class AuditLogViews(BaseView):
    """ Views for :class:`kotti_audit.resources.CustomContent` """

    @view_config(name='audit-log', permission='view',
                 renderer='kotti_audit:templates/audit-log.pt')
    def default_view(self):
        """ Default view for :class:`kotti_audit.resources.CustomContent`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }

    @view_config(name="audit-api", permission="admin",
                 renderer="json")
    def api_dropbox(self):
        limit = int(self.request.params.get("limit", 50))
        offset = int(self.request.params.get("offset", 0))
        sort = self.request.params.get("sort", "creation_date")
        order = self.request.params.get("order", "desc")
        parent_id = self.context.id if self.context.__parent__ else 0
        query = self.request.params.get("search", None)

        nodes = Content.query;

        if parent_id != 0:
            nodes = nodes.filter(
                Content.path.ilike('{}%'.format(self.context.path)),
                Content.id != self.context.id
            )

        if query is not None:
            nodes = nodes.filter(Content.title.ilike("%{}%".format(query)))

        if order == 'asc':
            nodes = nodes.order_by(Content.__dict__.get(sort).asc())
        else:
            nodes = nodes.order_by(Content.__dict__.get(sort).desc())

        total_nodes = nodes.count()
        if offset > 0:
            nodes = nodes.offset(offset)
        if limit > 0:
            nodes = nodes.limit(limit)

        nodes_json = [{
            "title": f.title,
            "context": f.parent.title if f.parent is not None else '',
            "path": f.path,
            "url": f.path,
            "id": f.id,
            "creation_date": f.creation_date.strftime("%A %d. %B %Y - %I:%M%p %z ") or '',
            "modification_date": f.modification_date.strftime("%A %d. %B %Y - %I:%M%p %z ") or ''
        } for f in nodes]
        return {
            "rows": nodes_json,
            "total": total_nodes
        }

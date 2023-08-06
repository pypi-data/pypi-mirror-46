import re
from lxml import etree

from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_comment import views


class CommentTC(CubicWebTC):
    """Comment"""

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            self.b = cnx.create_entity('BlogEntry', title=u"yo", content=u"qu\'il est beau").eid
            cnx.commit()

    def test_schema(self):
        self.assertEqual(self.schema['comments'].rdef('Comment', 'BlogEntry').composite,
                         'object')

    def test_possible_views(self):
        # comment primary view priority
        with self.admin_access.web_request() as req:
            rset = req.create_entity('Comment', content=u"bouh!", comments=self.b).as_rset()
            self.assertIsInstance(self.vreg['views'].select('primary', req, rset=rset),
                                  views.CommentPrimaryView)
            self.assertIsInstance(self.vreg['views'].select('tree', req, rset=rset),
                                  views.CommentThreadView)

    def test_possible_actions(self):
        with self.admin_access.web_request() as req:
            req.create_entity('Comment', content=u"bouh!", comments=self.b)
            self.create_user(req, 'user')  # will commit
            rset = req.execute('Any X WHERE X is BlogEntry')
            actions = self.pactions(req, rset)
            self.assertIn(('reply_comment', views.AddCommentAction), actions)
            self.assertNotIn(('edit_comment', views.EditCommentAction), actions)
            rset = req.execute('Any X WHERE X is Comment')
            actions = self.pactions(req, rset)
            self.assertIn(('reply_comment', views.ReplyCommentAction), actions)
            self.assertIn(('edit_comment', views.EditCommentAction), actions)
            req.cnx.commit()

        with self.new_access('user').web_request() as req:
            rset = req.execute('Any X WHERE X is Comment')
            actions = self.pactions(req, rset)
            self.assertIn(('reply_comment', views.ReplyCommentAction), actions)
            self.assertNotIn(('edit_comment', views.EditCommentAction), actions)
            rset = req.execute('INSERT Comment X: X content "ho bah non!", X comments B WHERE B is Comment')
            req.cnx.commit()
            actions = self.pactions(req, rset)
            self.assertIn(('reply_comment', views.ReplyCommentAction), actions)
            self.assertIn(('edit_comment', views.EditCommentAction), actions)

        with self.new_access('anon').web_request() as req:
            rset = req.execute('Any X WHERE X is Comment')
            self.assertEqual(self.pactions(req, rset), [])

    def test_nonregr_possible_actions(self):
        with self.admin_access.web_request() as req:
            req.create_entity('Comment', content=u"bouh!", comments=self.b)
            req.create_entity('Comment', content=u"Yooo!", comments=self.b)
            # now two comments are commenting the blog
            b = req.entity_from_eid(self.b)
            rset = b.related('comments', 'object')
            self.assertEqual(len(rset), 2)
            self.assertTrue(self.vreg['actions'].select('reply_comment', req, rset=rset, row=0))
            self.assertTrue(self.vreg['actions'].select('reply_comment', req, rset=rset, row=1))

    def test_add_related_actions(self):
        with self.admin_access.web_request() as req:
            req.create_entity('Comment', content=u"bouh!", comments=self.b)
            self.create_user(req, 'user')  # will comit
            rset = req.execute('Any X WHERE X is Comment')
            self.assertEqual(self.pactions_by_cats(req, rset), [])
            req.cnx.commit()

        with self.new_access('user').web_request() as req:
            rset = req.execute('Any X WHERE X is Comment')
            self.assertEqual(self.pactions_by_cats(req, rset), [])

        with self.new_access('anon').web_request() as req:
            rset = req.execute('Any X WHERE X is Comment')
            self.assertEqual(self.pactions_by_cats(req, rset), [])

    def test_path(self):
        with self.admin_access.repo_cnx() as cnx:
            c1 = cnx.create_entity('Comment', content=u"oijzr", comments=self.b)
            itreec1 = c1.cw_adapt_to('ITree')
            c11 = cnx.create_entity('Comment', content=u"duh?", comments=c1)
            itreec11 = c11.cw_adapt_to('ITree')
            self.assertEqual(itreec1.path(), [self.b, c1.eid])
            self.assertEqual(itreec1.root().eid, self.b)
            self.assertEqual(itreec11.path(), [self.b, c1.eid, c11.eid])
            self.assertEqual(itreec11.root().eid, self.b)

    def test_comments_ascending_order(self):
        with self.admin_access.repo_cnx() as cnx:
            b = cnx.entity_from_eid(self.b)
            c1 = cnx.create_entity('Comment', content=u"one", comments=self.b)
            c11 = cnx.create_entity('Comment', content=u"one-one", comments=c1)
            c12 = cnx.create_entity('Comment', content=u"one-two", comments=c1)
            c2 = cnx.create_entity('Comment', content=u"two", comments=self.b)
            self.assertEqual([c.eid for c in b.reverse_comments],
                             [c1.eid, c2.eid])
            self.assertEqual([c.eid for c in c1.cw_adapt_to('ITree').children()],
                             [c11.eid, c12.eid])

    def test_subcomments_count(self):
        with self.admin_access.repo_cnx() as cnx:
            c1 = cnx.create_entity('Comment', content=u"one", comments=self.b)
            cnx.create_entity('Comment', content=u"one-one", comments=c1)
            c12 = cnx.create_entity('Comment', content=u"one-two", comments=c1)
            cnx.create_entity('Comment', content=u"two-one", comments=c12)
            self.assertEqual(c1.subcomments_count(), 3)

    def test_fullthreadtext_views(self):
        with self.admin_access.web_request() as req:
            c = req.create_entity('Comment', content=u"bouh!", comments=self.b)
            c2 = req.create_entity('Comment', content=u"""
some long <b>HTML</b> text which <em>should not</em> fit on 80 characters, so i'll add some extra xxxxxxx.
Yeah !""", content_format=u"text/html", comments=c)
            req.cnx.commit()  # needed to set author
            content = c2.view('fullthreadtext')
            # remove date
            content = re.sub('..../../.. ..:..', '', content)
            self.assertMultiLineEqual(content,
                          """\
> On  - admin wrote :
> bouh!

some long **HTML** text which _should not_ fit on 80 characters, so i'll add
some extra xxxxxxx. Yeah !


i18n_by_author_field: admin
url: http://testing.fr/cubicweb/blogentry/%s""" % self.b)
            # fullthreadtext_descending view
            self.assertMultiLineEqual('''On  - admin wrote :
bouh!
> On  - admin wrote :
> some long **HTML** text which _should not_ fit on 80 characters, so i\'ll add
> some extra xxxxxxx. Yeah !
> 

''',
                                  re.sub('..../../.. ..:..', '', c.view('fullthreadtext_descending')))

    def test_fulltext_view_markdown(self):
        with self.admin_access.web_request() as req:
            content = u'\n'.join([
                (u'some long *Markdown* text which **should not** fit on 80 '
                 u'characters, so i\'ll add some extra xxxxxxx. Yeah !'),
                u'',
                u'* and a',
                u'* list',
            ])

            comment = req.create_entity('Comment', content=content,
                                        content_format=u'text/markdown',
                                        comments=self.b)
            req.cnx.commit()
            content = comment.view('fulltext')
            content = re.sub('..../../.. ..:..', '', content)
            expected = '\n'.join([
                'On  - admin wrote :',
                'some long *Markdown* text which **should not** fit on 80 characters, so i\'ll add',
                'some extra xxxxxxx. Yeah !',
                '',
                '* and a',
                '* list',
                '',
            ])
            self.assertMultiLineEqual(content, expected)

    def test_edit_comment_form(self):

        def render_comment_form(req):
            rset = req.create_entity('Comment', content=u'test').as_rset()
            view = self.vreg['views'].select('editcommentform', req, rset=rset)
            return view.render()

        with self.new_access('anon').web_request() as req:
            body = render_comment_form(req)
            self.assertIn('You are not authenticated. Your comment will be anonymous', body)
        with self.admin_access.web_request() as req:
            body = render_comment_form(req)
            self.assertNotIn('You are not authenticated. Your comment will be anonymous', body)

    def test_rssitem_view(self):
        with self.admin_access.web_request() as req:
            c1 = req.create_entity('Comment', content=u'foo', comments=self.b)
            c2 = req.create_entity('Comment', content=u'foo', comments=c1)
            c1.cw_set(comments=c2)
            xmldata = '<items>' + c1.view('rssitem') + '</items>'
            doc = etree.fromstring(xmldata, etree.XMLParser(recover=True))
            self.assertEqual(
                [node.text for node in doc.xpath('//guid')], [
                    'http://testing.fr/cubicweb/comment/{}'.format(c1.eid),
                    'http://testing.fr/cubicweb/comment/{}'.format(c2.eid),
                ])


if __name__ == '__main__':
    import unittest
    unittest.main()

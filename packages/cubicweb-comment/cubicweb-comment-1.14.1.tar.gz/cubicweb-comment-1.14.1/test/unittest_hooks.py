from cubicweb.devtools.testlib import CubicWebTC


class CommentViewsTC(CubicWebTC):

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            self.blog = cnx.create_entity('BlogEntry', title=u"une news !", content=u"cubicweb c'est beau").eid
            cnx.create_entity('Comment', content=u"Yo !")
            cnx.execute('SET C comments B WHERE B title "une news !", C content "Yo !"')
            cnx.commit()

    def test_notif_after_add_relation_comments(self):
        with self.admin_access.web_request() as req:
            c = req.execute('Comment X').get_entity(0, 0)
            v = self.vreg['views'].select('notif_after_add_relation_comments', req,
                                          rset=c.cw_rset, row=0)
            content = v.render(row=0)
            self.assertMultiLineEqual(content,
                          '''Yo !


i18n_by_author_field: admin
url: http://testing.fr/cubicweb/blogentry/%s''' %
                          c.comments[0].eid)
            self.assertEqual(v.subject(), 'new comment for BlogEntry une news !')


if __name__ == '__main__':
    import unittest
    unittest.main()

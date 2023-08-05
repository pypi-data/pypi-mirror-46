import requests
from os.path import basename
from urllib.parse import urlparse
from datetime import date
import json


class Comment:

    hasParentComment = False

    def __init__(self, article_url='', name='', email='', location='', title='', text='', likes=0, commentNum=0, commentDate=None, commentId=0, parentId=0):
        self.article = Article(article_url)
        self.name = name
        self.email = email
        self.location = location
        self.title = title
        self.text = text
        self.likes = likes
        self.commentNum = commentNum
        self.commentDate = commentDate
        self.commentId = commentId
        self.parentId = parentId
        if parentId != 0:
            self.hasParentComment = True

    def GetReplies(self):
        all_comments = self.article.GetComments()
        replies = []
        for comment in all_comments:
            if comment.parentId == self.commentId:
                replies.append(comment)
        return replies

    def GetParentComment(self):
        all_comments = self.article.GetComments()
        for comment in all_comments:
            if self.parentId == comment.commentId:
                return comment

    def Reply(self, comment):
        r = requests.post(self.article.article_uri +
                         'YediothPortal/Ext/TalkBack/CdaTalkBackTrans/0,2499,' +
                         self.article.article_id +
                         '-0-68-13108-0---' +
                         str(self.commentId) +
                         ',00.html', data={'WSGBRWSR':'FF',
                                             'name': comment.name,
                                             'email': comment.email,
                                             'Location': comment.location,
                                             'title': comment.title,
                                             'description': comment.text})
        return r.text
    
    def Post(self, useragent=
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"):
        r = requests.post(self.article.article_uri +
                          'YediothPortal/Ext/TalkBack/CdaTalkBackTrans/0,2499,'
                          + self.article.article_id +
                          '-0-68-546-0---0,00.html', data={'WSGBRWSR': 'FF',
                                                            'name': self.name,
                                                            'email': self.email,
                                                            'Location': self.location,
                                                            'title': self.title,
                                                            'description': self.text}, headers={'User-Agent':useragent})
        return r.text


class Article:

    def __init__(self, article_url):
        self.article_url = article_url
        parsed_url = urlparse(article_url)
        self.article_id = basename(parsed_url.path).split(',')[2]
        self.article_uri = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    def GetComments(self):
        comments = []
        r = requests.get(self.article_uri + "Ext/Comp/ArticleLayout/Proc/ShowTalkBacksAjax/v2/0,12990,"+
                         self.article_id +
                         "-desc-68-0-1,00.html",
                         params={'User-Agent':
                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}).text
        comments_json = json.loads(r)['rows']
        for comment_dict in comments_json:
            _comment_date = comment_dict['the_date'].split('.')
            comment_date = date(year=int(_comment_date[2]),
                                month=int(_comment_date[1]),
                                day=int(_comment_date[0]))
            comments.append(Comment(article_url=self.article_url,
                                    name=comment_dict['name'],
                                    title=comment_dict['title'],
                                    text=comment_dict['text'],
                                    location=comment_dict['location'],
                                    commentDate=comment_date,
                                    commentNum=comment_dict['tc'],
                                    likes=comment_dict['ts'],
                                    commentId=comment_dict['id'],
                                    parentId=comment_dict['parent_id']
                                    
                ))
        return comments     

    def GetCommentByCommentNum(self, commentNum):
        all_comments = self.GetComments()
        for comment in all_comments:
            if comment.commentNum == commentNum:
                return comment

    def GetCommentsByWriter(self, writerName):
        all_comments = self.GetComments()
        commentsByWriter = []
        for comment in all_comments:
            if comment.name == writerName:
                commentsByWriter.append(comment)
        return commentsByWriter

    def HasCommentsByWriter(self, writerName):
        if len(self.GetCommentsByWriter(writerName)) != 0:
            return True
        else:
            return False

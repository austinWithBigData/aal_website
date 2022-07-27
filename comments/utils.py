import logging

from djangoblog.utils import get_current_site
from djangoblog.utils import send_email

logger = logging.getLogger(__name__)


def send_comment_email(comment):
    site = get_current_site().domain
    subject = 'Thanks for your comment!'
    article_url = "https://{site}{path}".format(
        site=site, path=comment.article.get_absolute_url())
    html_content = """
                   <p>Thanks for your comment, </p>
                   you can visit 
                   <a href="%s" rel="bookmark">%s</a>
                    to check your comment. 
                   <br />
                   If you cannot open that link, please copy this link to the browser
                   %s
                   """ % (article_url, comment.article.title, article_url)
    tomail = comment.author.email
    send_email([tomail], subject, html_content)
    try:
        if comment.parent_comment:
            html_content = """
                    您在 <a href="%s" rel="bookmark">%s</a> 的评论 <br/> %s <br/> 收到回复啦.快去看看吧
                    <br/>
                    如果上面链接无法打开，请将此链接复制至浏览器。
                    %s
                    """ % (article_url, comment.article.title, comment.parent_comment.body, article_url)
            tomail = comment.parent_comment.author.email
            send_email([tomail], subject, html_content)
    except Exception as e:
        logger.error(e)

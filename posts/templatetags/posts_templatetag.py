from django import template
register = template.Library()
                                        # 이걸 만드는 목적: 해시태크 링크를 클릭하면 같은 해시태그를 사용한글이 보이게 해야하는데
                                        # 링크를 걸어주기 위해?? 아니면 같은 해시태크 사용글을 보이게 하려고?
@register.filter
def hashtag_link(post): # 함수명
    content = post.content # 
    hashtags = post.hashtags.all()
    
    for hashtag in hashtags:
        content = content.replace(hashtag.content, f'<a href="/posts/hashtag/{hashtag.id}/">{hashtag.content}</a>')
    return content


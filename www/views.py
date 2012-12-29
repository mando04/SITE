from django.shortcuts import render_to_response, RequestContext
from www.models import Post
from www.forms import modifyPost
from django.shortcuts import HttpResponseRedirect

def home(request):
    TITLE = "Welcome Home!"
    blog_p = Post.objects.all()
    content = {
    'TITLE': TITLE,
    'Post': blog_p,
    }
    return render_to_response('home.html', content, context_instance=RequestContext(request))


def postModify(request, post):
    if request.method == 'POST':
        f = modifyPost(request.POST)
        print f
        # load post
        p = Post.objects.get(id=post)
        p.title = f.title
        p.content = f.content
        p.save()
        return HttpResponseRedirect('/')
    else:
        print post
        TITLE = "Modify: '%s' post." % Post.objects.get(id=post).title
        p = Post.objects.get(id=post)
        f = modifyPost()
        content = {'forms': f,
                   'TITLE': TITLE,
                   'post': p,
        }
        return render_to_response("post/modify.html", content, context_instance=RequestContext(request))
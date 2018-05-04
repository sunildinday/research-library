from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
# from django.core.urlresolvers import reverse
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from .forms import DocumentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from user.models import Documents, Authors, KeyWord, Folder
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.template import RequestContext
import os
from django.conf import settings
# from user.forms import UserRegistrationForm

# used to submit the document


def index(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and request.FILES:
            post = {}
            post['user_id'] = request.user.id
            post['title'] = request.POST['title'].title()
            post['abstract'] = request.POST['abstract'].title()
            post['publisher'] = request.POST['publisher'].title()
            post['visibilty'] = request.POST['visibilty']
            post['branch'] = request.POST['branch']
            post['folder_label'] = request.POST['labels']
            label = request.POST['labels']
            form = DocumentForm(post, request.FILES)
            if form.is_valid():
                curr = form.save()
                tags = request.POST['tags']
                tags = tags.split(",")
                for tag in tags:
                    key = KeyWord(key=tag, document=curr)
                    key.save()
                authors = request.POST['author']
                authors = authors.split(",")
                for author in authors:
                    print(author)
                    writer = Authors(author=author, document=curr)
                    writer.save()
                request.session['alert'] = True
                return HttpResponseRedirect(reverse('user:dashboard', kwargs={'label': label, }))
                return render(request, 'user/done.html', {'msg': "Successfully Saved"},)
        else:
            form = DocumentForm()
            user_id = request.user.id
            label = Folder.objects.filter(user_id=user_id)
            error = None
            print("hiii")
            print(len(label))
            if len(label) == 0:
                error = 'First go to dashbooard and create a folder'

            return render(request, 'user/submit.html', {'form': form, 'labels': label, 'error_msg': error, })
    else:
        return render(request, 'user/login.html')


def logout_user(request):
    logout(request)
    form = UserLoginForm(request.POST or None)
    return render(request, 'user/login.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        # return HttpResponse(Documents._)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                user_id = request.user.id

                try:
                    document = Documents.objects.filter(user_id=user_id)
                except:
                    document = None
                return HttpResponseRedirect(reverse('user:dashboard_folder'))
            else:
                return render(request, 'user/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'user/login.html', {'error_message': 'Invalid login'})

    return render(request, 'user/login.html')


def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        form.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                f = Folder(label="Books", user_id=user.id)
                f.save()
                return render(request, 'user/dashboard.html', {'name': username})
    return render(request, 'user/register.html', {'form': form})


@login_required
def search(request):
    if request.user.is_authenticated():
        current_user = request.user
        return render(request, 'user/search.html', {'user': current_user})
    else:
        return render(request, 'user/login.html')


@login_required
def query(request):
    if request.user.is_authenticated():
        q = request.GET['q']
        search_by = request.GET['search_option']
        if q == "":
            q = "!#!B(IOSDOJI@!(*SOSasdndjsaoi j2u90usadsa d -sdusad 00828y0ds d0sysya d0say d0syd"
        try:
            if(search_by == "By Title"):
                document = Documents.objects.filter(Q(title__icontains=q) & Q(visibilty="PUBLIC"))
                # document = Documents.objects.get_by_title_and_id(q, user_id)
            elif(search_by == "By Author"):
                document = Documents.objects.filter(visibilty="PUBLIC")
                ans = []
                for doc in document:
                    qs = Authors.objects.filter(document=doc).filter(author__icontains=q).count()
                    if qs >= 1:
                        ans.append(doc)
                document = ans
            else:
                document = Documents.objects.filter(visibilty="PUBLIC")
                ans = []
                for doc in document:
                    qs = KeyWord.objects.filter(document=doc).filter(key__icontains=q).count()
                    if qs >= 1:
                        ans.append(doc)
                document = ans
        except:
            document = None

        if not document:
            msg = "Empty Search Result"
            return render(request, 'user/query.html', {'results': document, 'msg': msg})
        return render(request, 'user/query.html', {'results': document, })
    else:
        return render(request, 'user/login.html')


@login_required
def dashboard_folder(request):
    user_id = request.user.id
    folder = Folder.objects.filter(user_id=user_id)

    for fold in folder:
        label = fold.label
        count = Documents.objects.filter(Q(user_id=user_id) & Q(folder_label=label)).count()

        fold.total_count = count
    return render(request, 'user/dashboard_labels.html', {'result': folder})


@login_required
def dashboard(request, label):
    user_id = request.user.id
    print(request)
    authors_data = None
    document = None
    alert = None

    try:

        if request.session["alert"] == True:
            alert = "show"
            request.session["alert"] = False

        document = Documents.objects.filter(Q(user_id=user_id) & Q(folder_label=label))
        authors_data = ["bye"]
        for docu in document:
            authors = Authors.objects.all().filter(document=docu)
            auth_seq = []
            for auth in authors:
                auth_seq.append(auth.author)
            authors = ",".join(map(str, auth_seq))
            docu.author = authors

    except:
        document = None
    return render(request, 'user/dashboard.html', {'results': document, 'author': authors_data, 'user': user_id, 'alert': alert, 'label': label})


@csrf_protect
@login_required
def ajax_dashboard(request):
    if request.is_ajax():
        q = request.GET.get('q')
        search_by = request.GET.get('option')
        label = request.GET.get('label')
        user_id = request.user.id
        if q == "":
            q = "!#!B(IOSDOJI@!(*SOSasdndjsaoi j2u90usadsa d -sdusad 00828y0ds d0sysya d0say d0syd"
        try:
            if(search_by == "By Title"):
                document = Documents.objects.filter(Q(title__icontains=q) & Q(user_id__icontains=user_id) & Q(folder_label=label))
                # document = Documents.objects.get_by_title_and_id(q, user_id)
            elif(search_by == "By Author"):
                document = Documents.objects.filter(Q(user_id__icontains=user_id) & Q(folder_label=label))
                ans = []
                for doc in document:
                    qs = Authors.objects.filter(document=doc).filter(author__icontains=q).count()
                    if qs >= 1:
                        ans.append(doc)
                document = ans
            else:
                document = Documents.objects.filter(Q(user_id__icontains=user_id) & Q(folder_label=label))
                ans = []
                for doc in document:
                    qs = KeyWord.objects.filter(document=doc).filter(key__icontains=q).count()
                    if qs >= 1:
                        ans.append(doc)
                document = ans
        except:
            document = None
        ajax = True

        html = (render(request, 'user/dashboard_result.html', {'results': document, 'ajax': ajax}).content).decode('utf-8')

        data = {'hi': html}
        return JsonResponse(data)
        # return HttpResponse({'doc':document})
        return render(request, 'user/dashboard_result.html', {'results': document, 'ajax': ajax})


# used to toggle the private and public visibilty of  a document
@login_required
def toggle(request):
    if request.is_ajax():
        mode = request.GET.get('mode')
        document_id = request.GET.get('document_id')
        user_id = request.user.id
        document = Documents.objects.get(id=document_id, user_id=user_id)
        if mode == "PUBLIC":
            document.visibilty = "PRIVATE"
        else:
            document.visibilty = "PUBLIC"
        document.save()
        data = {'id': document.visibilty}
        return JsonResponse(data)


@login_required
def about(request):
    return render(request, 'user/about.html')


@login_required
def bibtex(request):

    if request.FILES:

        files = request.FILES[list(request.FILES.keys())[0]]

        bibtex_str = str(files.read())
        post = {}
        index1 = bibtex_str.find('title=')
        if index1 != -1:
            index2 = bibtex_str.find('}', index1)
            post['title'] = bibtex_str[index1 + 7:index2]

        index1 = bibtex_str.find('author=')
        if index1 != -1:
            index2 = bibtex_str.find('}', index1)
            post['author'] = bibtex_str[index1 + 8:index2]

        index1 = bibtex_str.find('abstract=')
        if index1 != -1:
            index2 = bibtex_str.find('}', index1)
            post['abstract'] = bibtex_str[index1 + 10:index2]

        index1 = bibtex_str.find('publisher=')

        if index1 != -1:
            index2 = bibtex_str.find('}', index1)
            post['publisher'] = bibtex_str[index1 + 11:index2]

        form = DocumentForm(post)

        return render(request, 'user/home.html', {'form': form, })


# view to check for duplicates
@login_required
def checker(request):
    if request.is_ajax():
        title = request.GET.get('title')
        author = request.GET.get('author')
        if author == "":
            author = "#@!@#$@@!@!@!@!@@ sadbhias hdsai dhias dhasui hdius"
        if title == "":
            title = "#@!@#$@@!@!@!@!@@ sdad sad sadsad sadsadsad"
        try:
            document = Documents.objects.filter(Q(title__icontains=title) & Q(author__icontains=author))

        except:
            document = None
        msg = {'msg': "", }

        if document:
            msg = {"msg": "Duplicate File with same author and title"}
            # return JsonResponse(msg)
        return JsonResponse(msg)


@csrf_protect
@login_required
def editpost(request, post_id=0):
    if request.method == 'GET':
        instance = get_object_or_404(Documents, id=post_id)
        form = DocumentForm(instance=instance)
        authors = Authors.objects.all().filter(document=instance)
        auth_seq = []
        for auth in authors:
            auth_seq.append(auth.author)
        authors = ",".join(map(str, auth_seq))

        tags = KeyWord.objects.all().filter(document=instance)
        tag_seq = []
        for tag in tags:
            tag_seq.append(tag.key)
        tags = ",".join(map(str, tag_seq))
        user_id = request.user.id
        label = Folder.objects.filter(user_id=user_id)
        return render(request, 'user/editpost.html',
             {'form': form, 'id': post_id, 'author': authors, 'tags': tags, 'labels': label})

    else:
        logout_user(request)


@csrf_protect
@login_required
def savepost(request):
    if request.method == 'POST':
        instance = get_object_or_404(Documents, id=request.POST['doc_id'])
        post = {}
        post['user_id'] = request.user.id
        post['title'] = request.POST['title'].title()
        post['abstract'] = request.POST['abstract'].title()
        post['publisher'] = request.POST['publisher'].title()
        post['visibilty'] = request.POST['visibilty']
        post['branch'] = request.POST['branch']
        post['folder_label'] = request.POST['labels']
        form = DocumentForm(post, instance=instance)
        if form.is_valid():
            curr = form.save()
            tags = request.POST['tags']
            tags = tags.split(",")
            KeyWord.objects.all().filter(document=instance).delete()
            for tag in tags:
                key = KeyWord(key=tag, document=curr)
                key.save()
            authors = request.POST['author']
            authors = authors.split(",")
            Authors.objects.all().filter(document=instance).delete()
            for author in authors:
                writer = Authors(author=author, document=curr)
                writer.save()
            return render_to_response('user/done.html', {'msg': "Successfully Updated"}, RequestContext(request))
        else:
            logout_user(request)
    else:
        logout_user(request)


@login_required
def download(request, post_id=0):

    document_id = post_id
    user_id = request.user.id
    document = Documents.objects.filter(id=document_id, user_id=user_id).values("document", "downloads")
    doc = Documents.objects.get(id=document_id, user_id=user_id)
    doc.downloads = doc.downloads + 1
    doc.save()
    path = document[0]['document']
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def delete_doc(request, post_id):
    document_id = post_id
    user_id = request.user.id
    instance = get_object_or_404(Documents, id=document_id)
    instance.delete()
    return render_to_response('user/done.html', {'msg': "Deleted"}, RequestContext(request))


# check for duplicate folder name
def check_label(request):
    if request.is_ajax():
        label = request.GET.get('q')
        user_id = request.user.id
        data = Folder.objects.filter(Q(user_id=user_id) & Q(label__iexact=label)).count()
        print(data)
        if data is not 0:
            msg = {'data': "true"}
        else:
            msg = {'data': "false"}

        return JsonResponse(msg)

# used to create a new folder


def create_label(request):
    if request.method == "POST":
        user_id = request.user.id
        label = request.POST['label']
        f = Folder(user_id=user_id, label=label)
        f.save()
        return HttpResponseRedirect(reverse('user:dashboard_folder'))
        return redirect(dashboard_folder)
        return render(request, 'user/dashboard_labels.html')


def edit_folder(request, label):
    if request.method == "POST":
        user_id = request.user.id
        new_label = request.POST['label']
        print(new_label)
        folder = Folder.objects.get(Q(user_id=user_id) & Q(label=label))
        folder.label = new_label
        folder.save()

        document = Documents.objects.filter(Q(user_id=user_id) & Q(folder_label=label))
        for doc in document:
            doc.folder_label = new_label
            doc.save()
        return HttpResponseRedirect(reverse('user:dashboard_folder'))
    else:
        return render(request, 'user/edit_folder.html', {'label': label})


@login_required
def authenticates(request):
    if request.method == "POST":
        user_id = request.user.id
        username = request.user.username
        password = request.POST['password']
        label = request.POST['label']
        user = authenticate(username=username, password=password)
        if user is not None:
            folder = get_object_or_404(Folder, user_id=user_id, label=label)
            folder.delete()
            document = Documents.objects.filter(user_id=user_id, folder_label=label)
            for doc in document:
                doc.delete()
            return HttpResponseRedirect(reverse('user:dashboard_folder'))
    return HttpResponseRedirect(reverse('user:logout_user'))

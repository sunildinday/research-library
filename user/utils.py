from user.models import Authors, KeyWord


def get_by_author(document, q):
    ans = []

    for doc in document:

        qs = Authors.objects.filter(document=doc).filter(author__icontains=q)
        if len(qs) >= 1:
            author = ""
            for auth in qs:
                author = author + auth.author
            doc.author = author
            ans.append(doc)
    return ans


def get_by_keyword(document):
    ans = []

    for doc in document:

        qs = Authors.objects.filter(document=doc)

        if len(qs) >= 1:
            author = ""
            for auth in qs:
                author = author + auth.author
            doc.author = author
            ans.append(doc)
    return ans


def get_keywords(document):
    for docu in document:
        tags = KeyWord.objects.all().filter(document=docu)
        tag_seq = []
        for tt in tags:
            tag_seq.append(tt.key)
            tags = ",".join(map(str, tag_seq))
            docu.tag = tags
    return document

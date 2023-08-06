from datetime import datetime


from canonicalwebteam.blog import wordpress_api as api
from canonicalwebteam.blog import logic
from canonicalwebteam.blog.common_view_logic import (
    get_index_context,
    get_article_context,
    get_group_page_context,
    get_topic_page_context,
)
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

tag_ids = settings.BLOG_CONFIG["TAG_IDS"]
excluded_tags = settings.BLOG_CONFIG["EXCLUDED_TAGS"]
blog_title = settings.BLOG_CONFIG["BLOG_TITLE"]
tag_name = settings.BLOG_CONFIG["TAG_NAME"]


def index(request):
    page_param = request.GET.get("page", default="1")
    category_param = request.GET.get("category", default="")

    try:
        if page_param == "1":
            featured_articles, total_pages = api.get_articles(
                tags=tag_ids,
                tags_exclude=excluded_tags,
                page=page_param,
                sticky="true",
                per_page=3,
            )
            featured_article_ids = [
                article["id"] for article in featured_articles
            ]
            articles, total_pages = api.get_articles(
                tags=tag_ids,
                tags_exclude=excluded_tags,
                exclude=featured_article_ids,
                page=page_param,
            )
        else:
            articles, total_pages = api.get_articles(
                tags=tag_ids, page=page_param, tags_exclude=excluded_tags
            )
            featured_articles = []

    except Exception as e:
        return HttpResponse("Error: " + e, status=502)

    context = get_index_context(
        page_param, articles, total_pages, featured_articles=featured_articles
    )
    context["title"] = blog_title
    context["category"] = {"slug": category_param}

    return render(request, "blog/index.html", context)


def group(request, slug, template_path):
    try:
        page_param = request.GET.get("page", default="1")
        category_param = request.GET.get("category", default="")

        group = api.get_group_by_slug(slug)
        group_id = group["id"]

        category_id = ""
        if category_param != "":
            category = api.get_category_by_slug(category_param)
            category_id = category["id"]

        articles, total_pages = api.get_articles(
            tags=tag_ids,
            tags_exclude=excluded_tags,
            page=page_param,
            groups=[group_id],
            categories=[category_id],
        )

    except Exception as e:
        return HttpResponse("Error: " + e, status=502)

    context = get_group_page_context(page_param, articles, total_pages, group)
    context["title"] = blog_title
    context["category"] = {"slug": category_param}

    return render(request, template_path, context)


def topic(request, slug, template_path):
    try:
        page_param = request.GET.get("page", default="1")

        tag = api.get_tag_by_slug(slug)

        articles, total_pages = api.get_articles(
            tags=tag_ids + [tag["id"]],
            tags_exclude=excluded_tags,
            page=page_param,
        )

    except Exception as e:
        return HttpResponse("Error: " + e, status=502)

    context = get_topic_page_context(page_param, articles, total_pages)
    context["title"] = blog_title

    return render(request, template_path, context)


def archives(request, template_path="blog/archives.html"):
    try:
        page = request.GET.get("page", default="1")
        category = request.GET.get("category", default="")
        group = request.GET.get("group", default="")
        month = request.GET.get("month", default="")
        year = request.GET.get("year", default="")

        groups = []
        categories = []

        if group:
            group = api.get_group_by_slug(group)
            groups.append(group["id"])

        if category:
            category = api.get_category_by_slug(category)
            categories.append(category["id"])

        after = ""
        before = ""
        if year:
            year = int(year)
            if month:
                month = int(month)
                after = datetime(year=year, month=month, day=1)
                before = after + relativedelta(months=1)
            else:
                after = datetime(year=year, month=1, day=1)
                before = datetime(year=year, month=12, day=31)

        articles, total_pages, total_posts = api.get_articles(
            tags=tag_ids,
            tags_exclude=excluded_tags,
            page=page,
            groups=groups,
            categories=categories,
            after=after,
            before=before,
        )

        if group:
            context = get_group_page_context(
                page, articles, total_pages, group
            )
        else:
            context = get_index_context(page, articles, total_pages)

        context["title"] = blog_title
        context["total_posts"] = total_posts

        return render(request, template_path, context)

    except Exception as e:
        return HttpResponse("Error: " + e, status=502)


def feed(request):
    try:
        feed = api.get_feed(tag_name)
    except Exception as e:
        return HttpResponse("Error: " + e, status=502)

    right_urls = logic.change_url(
        feed, request.build_absolute_uri().replace("/feed", "")
    )

    right_title = right_urls.replace("Ubuntu Blog", blog_title)

    return HttpResponse(right_title, status=200, content_type="txt/xml")


def article_redirect(request, slug, year=None, month=None, day=None):
    return redirect("article", slug=slug)


def article(request, slug):
    try:
        article = api.get_article(slug, tag_ids)
    except Exception as e:
        return HttpResponse("Error: " + e, status=502)

    if not article:
        return HttpResponseNotFound("Article not found")
    context = get_article_context(article, tag_ids)

    return render(request, "blog/article.html", context)


def latest_news(request):

    try:
        latest_pinned_articles = api.get_articles(
            tags=tag_ids,
            exclude=excluded_tags,
            page=1,
            per_page=1,
            sticky=True,
        )
        # check if the number of returned articles is 0
        if len(latest_pinned_articles[0]) == 0:
            latest_articles = api.get_articles(
                tags=tag_ids,
                exclude=excluded_tags,
                page=1,
                per_page=4,
                sticky=False,
            )
        else:
            latest_articles = api.get_articles(
                tags=tag_ids,
                exclude=excluded_tags,
                page=1,
                per_page=3,
                sticky=False,
            )

    except Exception:
        return JsonResponse({"Error": "An error ocurred"}, status=502)
    return JsonResponse(
        {
            "latest_articles": latest_articles,
            "latest_pinned_articles": latest_pinned_articles,
        }
    )

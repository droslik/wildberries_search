import asyncio
import pyexcel
from rest_framework import serializers
from .services import main


def data_handling(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    file = request.FILES
    article = request.data['article']
    if len(file) != 0 and article:
        raise serializers.ValidationError(
            'Only one option is possible: enter the article or attach the file'
        )
    if len(file) == 0 and not article:
        raise serializers.ValidationError(
            'Please enter correct article number or attach the file'
        )
    if len(file) > 0 and not article:
        task = loop.create_task(main(file_processing(request)))
        async_result = loop.run_until_complete(task)
        return async_result
    articles = [int(article)]
    task = loop.create_task(main(articles))
    async_result = loop.run_until_complete(task)
    if async_result is None:
        raise serializers.ValidationError('No results for your request')
    return async_result


def file_processing(request):
    filename = str(request.FILES['file'])
    extension = filename.split('.')[1]
    sheet = pyexcel.load_from_memory(extension, request.FILES['file'].read())
    articles_from_memory = sheet.to_array()
    articles = list(
        int(article[0]) for article in articles_from_memory
        if isinstance(article[0], int)
    )
    return articles

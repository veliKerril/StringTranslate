from django.http import HttpResponse
from django.shortcuts import render
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
from transliterate import translit
from string_script.models import Requests
import json


def string_script(text):
    duration = 3
    width = 100
    height = 100

    bg_clip = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)
    text_clip = TextClip(text, fontsize=40, color='white', font='Arial')
    text_clip.set_duration(duration)
    text_clip_width, text_clip_height = text_clip.size

    def translate(t):
        start_pos = (width / 2 - 15, height / 2 - text_clip_height / 2)
        end_pos = (width / 2 - text_clip_width, height / 2 - text_clip_height / 2)

        x = int(start_pos[0] + t / duration * (end_pos[0] - start_pos[0]))
        y = int(start_pos[1] + t / duration * (end_pos[1] - start_pos[1]))

        return x, y

    text_moving = text_clip.set_position(translate)
    video = CompositeVideoClip([bg_clip, text_moving]).set_duration(duration)
    video.write_videofile("moving_text.mp4", fps=60)


def main(request):
    if request.method == 'POST':
        json_headers = json.dumps(request.headers)
        r = Requests(method='POST', text=request.POST.get('text'), headers=json_headers)
        r.save()

        text = request.POST.get('text')
        string_script(text)

        path = 'moving_text.mp4'

        with open(f'{path}', 'rb') as f:
            data = f.read()

        name_of_video = translit(text.split()[0], language_code='ru', reversed=True)
        response = HttpResponse(data, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={name_of_video}.mp4'

        return response

    r = Requests(method='GET', headers=str(request.headers))
    r.save()
    return render(request, 'string_script/main_page.html')

from django.http import HttpResponse
from django.shortcuts import render
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
from transliterate import translit
from string_script.models import Requests
import json


def string_script(text, bg_color, text_color, font, v_size, v_time):
    duration = int(v_time)
    width = int(v_size)
    height = int(v_size)

    bg_clip = ColorClip(size=(width, height), color=tuple(map(int, bg_color.split(',')))).set_duration(duration)
    text_clip = TextClip(text, fontsize=int(v_size) * 0.4, color=text_color, font=font)
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

        print(request.POST)
        text = request.POST.get('text')
        bg_color = request.POST.get('bg_color', '0, 0, 0')
        text_color = request.POST.get('text_color', 'white')
        font = request.POST.get('font', 'Arial')
        v_size = request.POST.get('v_size', '100')
        v_time = request.POST.get('v_time', '3')

        # r = Requests(method='POST', text=request.POST.get('text'), headers=str(request.headers))
        # r.save()

        string_script(text, bg_color, text_color, font, v_size, v_time)

        path = 'moving_text.mp4'

        with open(f'{path}', 'rb') as f:
            data = f.read()

        name_of_video = translit(text.split()[0], language_code='ru', reversed=True)
        response = HttpResponse(data, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={name_of_video}.mp4'
        return response

    # r = Requests(method='GET', headers=str(request.headers))
    # r.save()
    return render(request, 'string_script/main_page.html')

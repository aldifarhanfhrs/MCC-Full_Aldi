import PySimpleGUI as sg
import io
import base64
from PIL import Image
import os.path
import cv2

BORDER_COLOR = '#194369'
DARK_HEADER_COLOR = '#112C45'
BPAD_LEFT = ((0, 2), (0, 2))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((0, 50))

img_HEIGHT = 650
img_WIDTH = 800
img_Setting = 400
image_SIZE = (img_WIDTH, img_HEIGHT)


def make_key(key):
    return {'default_text': sg.user_settings_get_entry(key, ''), 'key': key}


with open("logo MCC.png", "rb") as img_file:
    iconb64 = base64.b64encode(img_file.read())
icon = iconb64

with open("images.jpg", "rb") as img_file:
    image_data = base64.b64encode(img_file.read())
buffer = io.BytesIO()
imgdata = base64.b64decode(image_data)
img = Image.open(io.BytesIO(imgdata))
new_img = img.resize(image_SIZE)  # x, y
new_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue())


top_banner = [sg.Column([[
    sg.Text('MCC Vision System Checking' + ' ' * 66,
            font='Any 22', background_color=DARK_HEADER_COLOR),
    sg.Text('Tuesday 9 June 2020', font='Any 22',
            background_color=DARK_HEADER_COLOR)
]], size=(img_Setting + img_WIDTH + 30, 50), pad=((0, 0), (0, 0)), background_color=DARK_HEADER_COLOR
)]


cnt_image = [[sg.Image(data=img_b64, pad=(0, 0))]]

set_file_saving = [sg.Column(
    [
                  [sg.T('Image Saving',  font='_ 16',
                        background_color=BORDER_COLOR)],
                  [sg.CB('enable saving',  font='_ 14', enable_events=True, k='-isSaveFile-',
                         background_color=BORDER_COLOR, default=sg.user_settings_get_entry('-isSaveFile-', ''))],
                  [sg.T('File Location',  font='_ 12',
                        background_color=BORDER_COLOR)],
                  [sg.Input(sg.user_settings_get_entry('-locImage-', ''), key='-locImage-', enable_events=True,
                            disabled=True, use_readonly_for_disable=False,), sg.FolderBrowse()]
    ], pad=((0, 0), (0, 0)), background_color=BORDER_COLOR
)]

set_tcp_ip = [sg.Column(
    [
        [sg.T('TCP/IP configuration',  font='_ 16', background_color=BORDER_COLOR)],
        [sg.CB('enable TCP',  font='_ 14', enable_events=True, k='-isTCPActive-',
               background_color=BORDER_COLOR, default=sg.user_settings_get_entry('-isTCPActive-', ''))],
        [sg.T('TCP Server IP',  font='_ 12',
              background_color=BORDER_COLOR)],
        [sg.Input(sg.user_settings_get_entry('-IPSetting-', ''),
                  key='-IPSetting-'), sg.B('update', key='updateIpTcpServer')]
    ], pad=((0, 0), (0, 0)), background_color=BORDER_COLOR
)]

set_device_id = [sg.Column(
    [
        [sg.T('Device ID',  font='_ 16', background_color=BORDER_COLOR)],
        [sg.Input(sg.user_settings_get_entry('-deviceID-', ''),
                  key='-deviceID-'), sg.B('update', key='updateDevice')]
    ], pad=((0, 0), (0, 0)), background_color=BORDER_COLOR
)]

Set_Checking_enable = [sg.Column(
    [
        [sg.T('Checking Enable',  font='_ 16', background_color=BORDER_COLOR)],
        [sg.CB('enable Checking',  font='_ 14', enable_events=True, k='-isCheckEnable-',
               background_color=BORDER_COLOR, default=sg.user_settings_get_entry('-isCheckEnable-', ''))]
    ], pad=((0, 0), (0, 0)), background_color=BORDER_COLOR
)]

set_column = [sg.Column(
    [
        [sg.T('Checking Enable',  font='_ 16', background_color=BORDER_COLOR)]
    ]
)]
Set_result_text = sg.Column(
    set_column, element_justification='c', expand_x=True, expand_y=True)


cnt_setting = [set_file_saving,
               set_tcp_ip,
               set_device_id,
               Set_Checking_enable,
               Set_result_text
               ]

content_layout = [sg.Column(cnt_image, size=image_SIZE, pad=((10, 10), (10, 10))),
                  sg.Column(cnt_setting, size=(img_Setting, img_HEIGHT), pad=((0, 0), (0, 0)), background_color=BORDER_COLOR)]


layout = [top_banner, content_layout,
          [sg.Button('EXIT', button_color=('white', 'firebrick3'))]]

window = sg.Window('MCC Visual Inspection', layout, finalize=True,  resizable=True,
                   no_titlebar=True,
                   margins=(0, 0),
                   grab_anywhere=True,
                   icon=icon, location=(10, 10))

while True:
    event, values = window.read()
    if event == 'EXIT' or event == sg.WIN_CLOSED:
        break           # exit button clicked
    else:
        print(event)

    if event == '-locImage-':
        sg.user_settings_set_entry('-locImage-', values['-locImage-'])
    elif event == 'updateIpTcpServer':
        sg.user_settings_set_entry('-IPSetting-', values['-IPSetting-'])
    elif event == 'updateDevice':
        sg.user_settings_set_entry('-deviceID-', values['-deviceID-'])
    elif event == '-isTCPActive-':
        sg.user_settings_set_entry('-isTCPActive-', values['-isTCPActive-'])
    elif event == '-isSaveFile-':
        sg.user_settings_set_entry('-isSaveFile-', values['-isSaveFile-'])
    elif event == '-isCheckEnable-':
        sg.user_settings_set_entry(
            '-isCheckEnable-', values['-isCheckEnable-'])


window.close()

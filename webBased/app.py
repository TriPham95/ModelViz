#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:32:55 2020

@author: tpham
"""

import dash

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

app.config.suppress_callback_exceptions = True



external_css = [
    '/assets/style.css',
]
for css in external_css:
    app.css.append_css({"external_url": css})


@app.server.route('/assets/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(static_folder, path)



## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />
<%namespace name="base_meta" file="/base_meta.mako" />

<%def name="title()">Home</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .logo {
        text-align: center;
    }
    .logo img {
        margin: 3em auto;
    }
  </style>
</%def>

<div class="logo">
  ${h.image(image_url, "{} logo".format(capture(base_meta.app_title)), id='logo', width=500)}
  <h1>Welcome to ${base_meta.app_title()}</h1>
</div>

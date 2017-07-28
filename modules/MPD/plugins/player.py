from flask import render_template_string

class Player(object):
    has_panel = False
    button_index = 100
    button_label = ""
    index_template = """
{%- if stat -%}
    {%- if stat.state in (2, 3) -%}
        <br />
        {%- if current_song.is_stream -%}
            [Stream]{{ current_song.title }}
        {%- else -%}
            {{ current_song.formatted_title|safe }}
        {%- endif -%}
        <br />
        <table>
            <tr>
                <td>
                    <a id='sb' onclick='seekclick(event);'><div id='sbc' style='width:{{percent_time*2}}px'></div></a>
                </td>
                <td>
                    {{percent_time|int}}% - {{"%02d:%02d"|format(elapsed_time/60, elapsed_time%60)}}/<b>{{"%02d:%02d"|format(total_time/60, total_time%60)}}</b>
                </td>
            </tr>
        </table>
    {%- endif -%}
{%- else -%}
Error : Can't play that!
{%- endif -%}

<button class="uk-button" onclick='execute_plugin("player", "prev", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-fast-backward fa-2x" aria-hidden="true"></i></span></button>
{%- if stat.state != 2 -%}
    <button class="uk-button" onclick='execute_plugin("player", "play", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-play fa-2x" aria-hidden="true"></i></span></button>
{%- else -%}
    <button class="uk-button" onclick='execute_plugin("player", "pause", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-pause fa-2x" aria-hidden="true"></i></span></button>
{%- endif -%}
{%- if stat.state != 1 -%}
    <button class="uk-button" onclick='execute_plugin("player", "stop", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-stop fa-2x" aria-hidden="true"></i></span></button>
{%- endif -%}

<button class="uk-button" onclick='execute_plugin("player", "next", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-fast-forward fa-2x" aria-hidden="true"></i></span></button>

{%- if stat.state != 0 and stat.volume != -1 -%}
    <button class="uk-button" onclick='execute_plugin("player", "volume_down", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-volume-down fa-2x" aria-hidden="true"></i></span></button>
    <button class="uk-button" onclick='execute_plugin("player", "volume_up", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-volume-up fa-2x" aria-hidden="true"></i></span></button>
    <button class="uk-button"onclick='execute_plugin("player", "mute", {}, refresh_player);'><span class="fa-stack"><i class="fa fa-volume-off fa-stack-2x"></i><i class="fa fa-ban text-danger fa-stack-2x"></i></span></button>
             <span class="fa-stack fa-5x"><i class="fa fa-volume-off fa inverse fa-stack-1x"></i><strong class="fa-stack-1x fa-stack-text fa-inverse" style="font-size:11px">{{ stat.volume }}%</strong></span>
{%- endif -%}
"""
    playlist_template = """
<h2>Playlist ({{ total_index }})
    <button class="uk-button" onclick='execute_plugin("player", "clear", {}, refresh_player);'>clear</button>
    <button class="uk-button" onclick='execute_plugin("player", "clear_old", {}, refresh_player);'>clear old</button>
    <button class="uk-button" onclick='execute_plugin("player", "shuffle", {}, refresh_player);'>shuffle</button>
</h2>

{%- for index, entry in enumerate(playlist) -%}
    <li
    {%- if current_index == index+1 -%}
        class='s'
    {%- else -%}
        {{ loop.cycle("", "class='p'") }}
    {%- endif -%}
    >{{ "%03d"|format(index) }}<a href='#' onclick='execute_plugin("player", "delete", {idx: {{index}} }, refresh_player);'><i class="fa fa-trash-o fa-2x" aria-hidden="true"></i></a>
        <a href='#' onclick='execute_plugin("player", "play", {idx: {{index}} }, refresh_player);'>{{ entry.formatted_title }}</a>
    </li>
{%- endfor -%}

"""

    def __init__(self, mpd, config):
        self.config = config
        self.mpd = mpd

    def index(self):
        stat = self.mpd.status()
        if stat.state in (2,3):
            elapsed_time, total_time, percent_time = self.mpd.getSongPosition()
        else:
            elapsed_time, total_time, percent_time = 0, 0, 0

        return render_template_string(self.index_template, stat=stat, current_song=self.mpd.getCurrentSong(self.config['tag_format']), elapsed_time=elapsed_time, total_time=total_time, percent_time=percent_time, has_stream=self.config['has_stream'])

    def playlist(self):
        current_index, total_index = self.mpd.getPlaylistPosition()
        return render_template_string(self.playlist_template, current_index=current_index, total_index=total_index, playlist=self.mpd.playlist(self.config['tag_format']), enumerate=enumerate)

    def ajax_play(self, idx=None):
        if idx:
            self.mpd.play(int(idx))
        else:
            self.mpd.play()

    def ajax_delete(self, idx=None):
        self.mpd.delete([int(idx), ])
    
    def ajax_next(self):
        self.mpd.next()

    def ajax_prev(self):
        self.mpd.prev()

    def ajax_pause(self):
        self.mpd.pause()

    def ajax_playpause(self):
        stat = self.mpd.status()
        if stat.state != 2:
            self.mpd.play()
        else:
            self.mpd.pause()

    def ajax_stop(self):
        self.mpd.stop()

    def ajax_clear(self):
        self.mpd.clear()

    def ajax_clear_old(self):
        idx, tot = self.mpd.getPlaylistPosition()
        self.mpd.delete([[0, max(0, idx-2)]])

    def ajax_shuffle(self):
        self.mpd.shuffleIt()

    def ajax_seek(self, percent=None):
        self.mpd.seek(percent=int(percent))

    def ajax_volume_up(self):
        self.mpd.volumeUp()

    def ajax_volume_down(self):
        self.mpd.volumeDown()
    
    def ajax_mute(self):
        self.mpd.mute()

    def ajax_change_display(self, idx=None):
        self.mpd.changeDisplay(int(idx))

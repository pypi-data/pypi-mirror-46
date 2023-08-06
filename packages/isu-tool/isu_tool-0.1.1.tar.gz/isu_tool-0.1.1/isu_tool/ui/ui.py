import time, sys, os

def pgbar(
        data,
        pre='',
        post='',
        bar_icon='=',
        space_icon=' ',
        total_display=1000,
        show_running_time=True,
        show_eta=True,
        time_format='%02dh%02dm%02ds',
        show_percent=True,
        show_cnt=True,
        end='\r',
        size=None):
    ' PRE[PGBAR] [000%|0000/0000] [00h00m00s/00h00m00s]POST '
    
    if not size:
        size = len(data)

    start_time = time.time()

    for i, d in enumerate(data):
        tsize, _ = os.get_terminal_size()
        bsize = tsize - len(pre) - len(post) - 7

        if show_running_time:
            bsize -= 12
            if show_eta:
                bsize -= 10
        if show_percent:
            bsize -= 6
            if show_cnt:
                bsize -= len(str(size)) * 2 + 2

        bar = bar_icon * (bsize * (i + 1) // size // len(bar_icon))
        space = space_icon * (bsize - len(bar))

        total_time = int(time.time() - start_time)
        hour = total_time // 3600
        minute = total_time % 3600 // 60
        second = total_time % 60

        if total_time == 0:
            eta_time = 0
        else:
            eta_time = total_time * size / (i + 1)
        eta_hour = eta_time // 3600
        eta_minute = eta_time % 3600 // 60
        eta_second = eta_time % 60

        running_time = ''
        if show_running_time:
            running_time = time_format % (hour, minute, second)
            eta = time_format % (eta_hour, eta_minute, eta_second)
            if i == size - 1:
                eta = running_time
            if show_eta:
                running_time = ' [%s/%s]' % (running_time, eta)
            else:
                running_time = ' [%s]' % running_time

        percent = ''
        if show_percent:
            percent = '%3d%%' % (100 * (i + 1) // size)
            cnt_format = '%%%dd/%d' % (len(str(size)), size)
            cnt = cnt_format % (i + 1)
            if show_cnt:
                percent = ' [%s|%s]' % (percent, cnt)
            else:
                percent = ' [%s]' % percent

        if size < total_display or i % (size // total_display) == 0 or i == size - 1:
            print(' %s [%s%s]%s%s%s ' % (pre, bar, space, percent, running_time, post), end=end)
        if i == size - 1:
            print()

        yield d

        if i == size - 1:
            break


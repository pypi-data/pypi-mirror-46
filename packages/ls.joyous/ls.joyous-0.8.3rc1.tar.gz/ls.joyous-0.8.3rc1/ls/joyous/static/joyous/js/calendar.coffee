#---------------------------------------------------------------------------
# Calendar scripts
#---------------------------------------------------------------------------

class EventsCalendar
    constructor: () ->
        return

    enable: () ->
        @_enablePopup()
        $(window).resize () =>
            @_handleResize()
        @_handleResize()
        return

    _enablePopup: () ->
        if $("#calendar-overlay").length == 0
            $("""
  <div id="calendar-overlay"></div>
  <div class="day-popup-outer">
    <div id="read-more-events" class="calendar day-popup">
      <a class="close" href="#">×</a>
      <div class="day-title"></div>
      <div class="days-events"></div>
    </div>
  </div>""").appendTo("body")
        $("#calendar-overlay, .day-popup-outer, .day-popup .close").click () ->
            $("#calendar-overlay, .day-popup-outer").hide()
            return false
        $(".day-popup").click (event) ->
            event.stopPropagation()

    _handleResize: () ->
        if $("tbody").hasClass("monthly-view")
            @_adjustDays()
        @_linkReadMore()

    _adjustDays: () ->
        width = $("tbody.monthly-view td.day .day-title").first().outerWidth()
        height = $("tbody.monthly-view td.day .day-title").first().outerHeight()
        eventsHeight = (width - height - 1) * 0.71
        $("tbody.monthly-view .days-events").outerHeight(eventsHeight)
        return

    _linkReadMore: () ->
        $(".days-events").each (index, element) =>
            day = $(element).closest("td.day")
            day.find("a.read-more").remove()
            if (element.offsetHeight < element.scrollHeight or
                 element.offsetWidth < element.scrollWidth)
                @_addReadMoreLink(day)
            return
        return

    _addReadMoreLink: (day) ->
        link = $("<a>").attr('href', 'javascript:void 0')
                       .attr('title', "Show all of this day's events")
                       .addClass("read-more").text("+")
        link.click (ev) ->
            title = day.find(".day-title").clone()
            $("#read-more-events .day-title").replaceWith(title)
            events = day.find(".days-events").clone().height('auto')
            $("#read-more-events .days-events").replaceWith(events)
            y = Math.max(ev.pageY - 100, $(window).scrollTop())
            $(".day-popup-outer").css('top', y)
            $("#calendar-overlay, .day-popup-outer").show()
            return false
        day.append(link)
        return


$ ->
    calendar = new EventsCalendar()
    calendar.enable()
    return



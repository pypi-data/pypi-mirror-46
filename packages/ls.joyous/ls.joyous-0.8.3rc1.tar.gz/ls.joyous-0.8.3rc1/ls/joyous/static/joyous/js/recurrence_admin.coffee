#---------------------------------------------------------------------------
# Recurrence Widget
#---------------------------------------------------------------------------
$ = @$ ? django.jQuery

class RecurrenceWidget
    constructor: (widgetId) ->
        ourDiv = $("##{widgetId}")
        @our = ourDiv.find.bind(ourDiv)
        @_init()
        return

    _init: () ->
        showAdvanced = @_hasAdvanced()
        @our(".ev-show-advanced-cbx").prop("checked", showAdvanced)
        @our(".ev-advanced-repeat").toggle(showAdvanced)
        freq = @our(".ev-freq-choice > select").val()
        @_freqChanged(freq)
        @_primaryOrdDayChanged()
        return

    _hasAdvanced: () ->
        interval = @our(".ev-interval-num > input").val()
        if interval and parseInt(interval, 10) > 1
            return true

        weekdaysTicked = @our(".ev-weekdays :checkbox:checked").map ->
            return this.value
        .get()
        if weekdaysTicked.length > 1
            return true
        dtstart = new Date(@our(".ev-start-date > input").val())
        weekday = (dtstart.getDay() + 6) % 7  # convert from Sun=0 to Mon=0
        if weekdaysTicked.length == 1 and parseInt(weekdaysTicked[0], 10) != weekday
            return true

        month = dtstart.getMonth() + 1
        monthsTicked = @our(".ev-months :checkbox:checked").map ->
            return this.value
        .get()
        if monthsTicked.length > 1
            return true
        if monthsTicked.length == 1 and parseInt(monthsTicked[0], 10) != month
            return true

        ordChoice = @our(".ev-primary .ev-ord-choice > select").val()
        if parseInt(ordChoice, 10) != 101
            return true
        dayChoice = @our(".ev-primary .ev-day-choice > select").val()
        if parseInt(dayChoice, 10) != 200
            return true
        secondaryOrdDaySet = $(".ev-secondary select").is ->
            return $(this).val() != ""
        if secondaryOrdDaySet
            return true
        return false

    _clearAdvanced: () ->
        @our(".ev-interval-num > input").val(1)
        @our(".ev-weekdays :checkbox").prop("checked", false)
        @our(".ev-months :checkbox").prop("checked", false)
        dtstart = new Date(@our(".ev-start-date > input").val())
        weekday = (dtstart.getDay() + 6) % 7  # convert from Sun=0 to Mon=0
        @our(".ev-weekdays :checkbox[value=#{weekday}]").prop("checked", true)
        @our(".ev-primary .ev-ord-choice > select").val(101)
        @our(".ev-primary .ev-day-choice > select").val(200)
        @our(".ev-secondary select").val("").prop('disabled', true)
        return

    enable: () ->
        @_enableShowAdvanced()
        @_enableStartDateChange()
        @_enableFreqChange()
        @_enableSecondaryOrdDayClear()
        @_enablePrimaryOrdDayChange()
        return

    _enableShowAdvanced: () ->
        @our(".ev-show-advanced-cbx").click (ev) =>
            if $(ev.target).prop("checked")
                @our(".ev-advanced-repeat").show()
            else
                @our(".ev-advanced-repeat").hide()
                @_clearAdvanced()
            return true
        return

    _enableStartDateChange: () ->
        @our(".ev-start-date > input, .ev-").change (ev) =>
            showAdvanced = @our(".ev-show-advanced-cbx").prop("checked")
            if not showAdvanced
                @_clearAdvanced()
            return false
        return

    _enableFreqChange: () ->
        @our(".ev-freq-choice > select").change (ev) =>
            @_freqChanged($(ev.target).val())
            @_clearAdvanced()
            return false
        return

    _enableSecondaryOrdDayClear: () ->
        @our(".ev-secondary .ev-ord-choice > select").change (ev) =>
            if $(ev.target).find("option:selected").val() == ""
                row = $(ev.target).closest(".ev-double-field")
                row.find(".ev-day-choice > select").val("")
            return false
        @our(".ev-secondary .ev-day-choice > select").change (ev) =>
            if $(ev.target).find("option:selected").val() == ""
                row = $(ev.target).closest(".ev-double-field")
                row.find(".ev-ord-choice > select").val("")
            return false
        return

    _enablePrimaryOrdDayChange: () ->
        @our(".ev-primary select").change (ev) =>
            @_primaryOrdDayChanged()
            return false
        return

    _primaryOrdDayChanged: () ->
        ord = @our(".ev-primary .ev-ord-choice option:selected").val()
        day = @our(".ev-primary .ev-day-choice option:selected").val()
        if -1 <= parseInt(ord, 10) <= 5 and 0 <= parseInt(day, 10) <= 6
            # enable and clauses
            @our(".ev-secondary select").prop('disabled', false)
        else
            @our(".ev-secondary select").val("").prop('disabled', true)

        return

    _freqChanged: (freq) ->
        visible = [false, false, false]
        frequency = parseInt(freq, 10)
        switch frequency
            when 3
                visible = [false, false, false]
            when 2
                visible = [true,  false, false]
            when 1
                visible = [false, true,  false]
            when 0
                visible = [false, true, true]
        @our(".ev-advanced-weekly-repeat").toggle(visible[0])
        @our(".ev-advanced-monthly-repeat").toggle(visible[1])
        @our(".ev-advanced-yearly-repeat").toggle(visible[2])
        @our(".ev-interval-units-days").toggle(frequency==3)
        @our(".ev-interval-units-weeks").toggle(frequency==2)
        @our(".ev-interval-units-months").toggle(frequency==1)
        @our(".ev-interval-units-years").toggle(frequency==0)
        return

@initRecurrenceWidget = (id) ->

    widget = new RecurrenceWidget(id)
    widget.enable()
    return

@initExceptionDateChooser = (id, validDates, opts) ->
    dtpOpts =
        onGenerate: (ct) ->
            past = new Date()
            past.setDate(past.getDate()-200)
            past.setDate(1)
            future = new Date()
            future.setDate(future.getDate()+600)
            future.setDate(1)
            if validDates != null and past < ct < future
                #console.log(ct)
                $(this).find('td.xdsoft_date').addClass('xdsoft_disabled')
                for yyyymmdd in validDates
                    yyyy = parseInt(yyyymmdd[0...4], 10)
                    mm   = parseInt(yyyymmdd[4...6], 10) - 1
                    dd   = parseInt(yyyymmdd[6...8], 10)
                    $(this).find("td.xdsoft_date[data-year=#{yyyy}][data-month=#{mm}][data-date=#{dd}]")
                           .removeClass('xdsoft_disabled')
        closeOnDateSelect: true
        timepicker:        false
        scrollInput:       false
        format:            'Y-m-d'
        dayOfWeekStart:    0
    $.extend(dtpOpts, opts)
    $('#' + id).datetimepicker(dtpOpts)

odoo.define('web_enterprise.CalendarRenderer', function (require) {
"use strict";

const config = require('web.config');
if (!config.device.isMobile) {
    return;
}

/**
 * This file implements some tweaks to improve the UX in mobile.
 */

const {qweb} = require('web.core');

const CalendarRenderer = require('web.CalendarRenderer');

// FIXME: in the future we should use modal instead of popover (on Event Click)
CalendarRenderer.include({

    events: _.extend({}, CalendarRenderer.events, {
        'click .o_other_calendar_panel': '_toggleSidePanel',
    }),

    /**
     * @constructor
     * @param {Widget} parent
     * @param {Object} state
     * @param {Object} params
     */
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        this.isSwipeEnabled = true;
        this.isSidePanelVisible = false;
        this.filtersMobile = [];
    },
    on_attach_callback: function () {
        this.$el.height($(window).height() - this.$el.offset().top);
        this._super(...arguments);
    },
    /**
     * @override
     * @returns {Promise}
     */
    start: function () {
        const promise = this._super();
        this._bindSwipe();
        return promise;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Bind handlers to enable swipe navigation
     *
     * @private
     */
    _bindSwipe: function () {
        const self = this;
        let touchStartX;
        let touchEndX;
        this.calendarElement.addEventListener('touchstart', function (event) {
            self.isSwipeEnabled = true;
            touchStartX = event.touches[0].pageX;
        });
        this.calendarElement.addEventListener('touchend', function (event) {
            if (!self.isSwipeEnabled) {
                return;
            }
            touchEndX = event.changedTouches[0].pageX;
            if (touchStartX - touchEndX > 100) {
                self.trigger_up('next');
            } else if (touchStartX - touchEndX < -100) {
                self.trigger_up('prev');
            }
        });
    },
    /**
     * Concat all filter available in side panel and filter the inactive
     *
     * @private
     * @return {[]}
     */
    _getFilters: function () {
        const filters = this.state.filters;
        return Object.keys(filters)
            .filter(key => filters[key].filters)
            .map(key => ({
                label: filters[key].title,
                values: this._prepareDataFilterForQWeb(filters[key].filters),
                countItems: filters[key].filters.length,
            }))
            ;
    },
    /**
     * In mobile we change the column header to avoid to much text
     *
     * @override
     * @private
     */
    _getFullCalendarOptions: function () {
        const oldOptions = this._super(...arguments);
        // Parameters
        oldOptions.views.dayGridMonth.columnHeaderFormat = 'ddd';
        oldOptions.weekNumbersWithinDays = false;
        oldOptions.views.dayGridMonth.weekLabel = '';
        // Event Listeners
        const oldEventDragStart = oldOptions.eventDragStart;
        const oldEventPositioned = oldOptions.eventPositioned;
        const oldEventRender = oldOptions.eventRender;
        const oldEventResize = oldOptions.eventResize;
        const oldEventResizeStart = oldOptions.eventResizeStart;
        const oldSelectAllow = oldOptions.selectAllow;
        const oldSelect = oldOptions.select;

        oldOptions.eventDragStart = (info) => {
            this.isSwipeEnabled = false;
            if (oldEventDragStart) {
                oldEventDragStart.call(this.calendar, info);
            }
        };
        oldOptions.eventPositioned = (info) => {
            this.isSwipeEnabled = false;
            if (oldEventPositioned) {
                oldEventPositioned.call(this.calendar, info);
            }
        };
        oldOptions.eventRender = (info) => {
            this.isSwipeEnabled = false;
            if (oldEventRender) {
                oldEventRender.call(this.calendar, info);
            }
        };
        oldOptions.eventResize = (eventResizeInfo) => {
            this.isSwipeEnabled = false;
            if (oldEventResize) {
                oldEventResize.call(this.calendar, eventResizeInfo);
            }
        };
        oldOptions.eventResizeStart = (mouseResizeInfo) => {
            this.isSwipeEnabled = false;
            if (oldEventResizeStart) {
                oldEventResizeStart.call(this.calendar, mouseResizeInfo);
            }
        };
        oldOptions.selectAllow = (selectInfo) => {
            this.isSwipeEnabled = false;
            if (oldSelectAllow) {
                return oldSelectAllow.call(this.calendar, selectInfo);
            }
            return true;
        };
        oldOptions.select = (selectionInfo) => {
            // Needed to avoid to trigger select and dateClick on long tap
            selectionInfo.jsEvent.isSelectiong = true;
            if (oldSelect) {
                return oldSelect.call(this.calendar, selectionInfo);
            }
        };
        // /!\ Override if dateClick is set in web module
        oldOptions.dateClick = (dateClickInfo) => {
            if (dateClickInfo.jsEvent.isSelectiong) {
                return;
            }
            const data = {start: dateClickInfo.date, allDay: dateClickInfo.allDay};
            this._preOpenCreate(data);
        };
        // TODO refactor year view to have consistency API (use dateClick instead of yearDateClick)
        oldOptions.yearDateClick = (yearDateClickInfo) => {
            this.trigger_up('changeDate', {
                date: moment(yearDateClickInfo.date),
                scale: 'day',
            });
        };

        return oldOptions;
    },
    /**
     * Prepare the parameters for the popover.
     * Setting the popover is append to the body
     * and so no need the use of z-index
     *
     * @private
     * @override method from CalendarRenderer
     * @param {Object} eventData
     */
    _getPopoverParams: function (eventData) {
        const popoverParameters = this._super.apply(this, arguments);
        popoverParameters.container = 'body';
        return popoverParameters;
    },
    /**
     * Finalise the popover
     * We adding some inline css to put the popover in a "fullscreen" mode
     *
     * @private
     * @override method from CalendarRenderer
     * @param {jQueryElement} $popoverElement
     * @param {web.CalendarPopover} calendarPopover
     */
    _onPopoverShown: function ($popoverElement, calendarPopover) {
        this._super.apply(this, arguments);
        const $popover = $($popoverElement.data('bs.popover').tip);
        // Need to be executed after Bootstrap popover
        // Bootstrap set style inline and so override the scss style
        setTimeout(() => {
            $popover.toggleClass([
                'bs-popover-left',
                'bs-popover-right',
            ], false);
            $popover.find('.arrow').remove();
            $popover.css({
                display: 'flex',
                bottom: 0,
                right: 0,
                borderWidth: 0,
                maxWidth: '100%',
                transform: 'translate3d(0px, 0px, 0px)',
            });
            $popover.find('.o_cw_body').css({
                display: 'flex',
                flex: '1 0 auto',
                flexDirection: 'column',
            });
            // We grow the "popover_fields_secondary" to have the buttons in the bottom of screen
            $popover.find('.o_cw_popover_fields_secondary')
                .toggleClass('o_cw_popover_fields_secondary', false)
                .css({
                        flexGrow: 1,
                    }
                );
            // We prevent the use of "scroll" events to avoid bootstrap listener
            // to resize the popover
            $popover.on('touchmove', (event) => {
                event.preventDefault();
            });
            // Firefox
            $popover.on('mousewheel', (event) => {
                event.preventDefault();
            });
            // Chrome
            $popover.on('wheel', (event) => {
                event.preventDefault();
            });
            // When the user click on a link the popover must be removed
            $popover
                .find('a.o_field_widget[href]')
                .on('click', (event) => {
                    $('.o_cw_popover').popover('dispose');
                });
        }, 0);
    },
    /**
     * Filter the inactive element and set the color
     *
     * @private
     * @param {[]} array
     * @return {[]}
     */
    _prepareDataFilterForQWeb: function (array) {
        const self = this;
        return array
            .filter(element => element.active)
            .map(function (element) {
                return Object.assign({}, element, {
                    color: self.getColor(element.color_index),
                });
            });
    },
    /**
     * Add a element to be able to manage other calendar in mobile
     *
     * @override
     */
    async _renderView() {
        return this._super(...arguments).then(() => {
            this.$('.o_calendar_mini').toggleClass('d-none', true);
            this._renderOtherCalendar();
        });
    },
    /**
     * Recalculate the filters for mobile view
     *
     * @private
     */
    _renderFilters: function () {
        return this._super(...arguments).then(() => {
            this.filtersMobile = this._getFilters();
            const reduce = !!this.filtersMobile.reduce((visible, filter) => visible | (filter.countItems > 0), false);
            this.$('.o_calendar_sidebar .o_view_nocontent').toggleClass('d-none', reduce);
        });
    },
    /**
     * Render the specific view for OtherCalendarPanel
     *
     * @private
     */
    _renderOtherCalendar: function () {
        this.$('.o_other_calendar_panel').remove();
        this.otherCalendarMobile = $(qweb.render('CalendarView.OtherCalendarMobile', {
            filters: this.filtersMobile,
            isSidePanelVisible: this.isSidePanelVisible,
        }));
        this.$el.prepend(this.otherCalendarMobile);
    },
    /**
     * Toggle the d-none class of calendar and side panel to switch between the two elements
     *
     * @private
     */
    _toggleSidePanel: async function () {
        this.isSidePanelVisible = !this.isSidePanelVisible;
        this.$('.o_calendar_view').toggleClass('d-none', this.isSidePanelVisible);
        this.$('.o_calendar_sidebar_container').toggleClass('d-none', !this.isSidePanelVisible);
        this._renderOtherCalendar();
    },
    /**
     * Remove highlight classes and dispose of popovers
     *
     * @private
     */
    _unselectEvent: function () {
        this._super.apply(this, arguments);
        $('.o_cw_popover').popover('dispose');
    },
});

});

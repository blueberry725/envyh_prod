(function ($) {

    "use strict";
    $.fn.rtMobileMenu = function (options) {

        var defaults = {
            target: $(this),
            menuHolder: "body",
            menuHolderId: "rt-mmenu-container",
            screenWidth: "991",
            menuClose: "X",
            siteLogo: '',
            siteLogoId: '',
            meanMenuOpen: "<span /><span /><span />",
            meanRevealPositionDistance: "0",
            showChildren: false,
            expandableChildren: true,
            meanExpand: "+",
            meanContract: "-",
            onePage: false,
            meanDisplay: "block",
            removeElements: ""
        };
        options = $.extend(defaults, options);

        var currentWidth = window.innerWidth || document.documentElement.clientWidth;
        var is_mobile = (navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i)) || (navigator.userAgent.match(/Android/i)) || (navigator.userAgent.match(/Blackberry/i)) || (navigator.userAgent.match(/Windows Phone/i));
        var screenWidth = options.screenWidth || 0;
        var logo = options.siteLogoId ? $("#" + options.siteLogoId).clone().html() : options.siteLogo;
        // this.centeMenu = function () {
        //     if (meanRevealPosition === "center") {
        //         var newWidth = window.innerWidth || document.documentElement.clientWidth;
        //         var meanCenter = ((newWidth / 2) - 22) + "px";
        //         meanRevealPos = "left:" + meanCenter + ";right:auto;";

        //         if (!isMobile) {
        //             jQuery('.meanmenu-reveal').css("left", meanCenter);
        //         } else {
        //             jQuery('.meanmenu-reveal').animate({
        //                 left: meanCenter
        //             });
        //         }
        //     }
        // };



        this.init = function () {

            return options.target.each(function () {
                var obj = {
                    rtMenuFlag: false,
                    targetMenu: $(this).clone(),
                    resetMenu: function () {
                        this.rtMenuFlag = false;
                        $('#' + options.menuHolderId).find('#rt-mmenu').remove().parent().attr("id", '');
                    },
                    createMenu: function () {
                        if (currentWidth <= screenWidth) {
                            this.rtMenuFlag = true;
                            $(options.menuHolder).attr("id", options.menuHolderId);
                            var menu = $('<div id="rt-mmenu" />');
                            if (logo) {
                                menu.addClass('rt-has-logo');
                                $('<div class="rt-mmneu-logo" />').append(logo).appendTo(menu);
                            }
                            var new_menu = $('<nav class="rt-mmenu-nav" />').append(this.getMenu(obj.targetMenu))
                            new_menu.find('nav.rt-mmenu-nav ul li').removeAttr("class").removeAttr("id");
                            new_menu.appendTo(menu);
                            menu.prependTo($('#' + options.menuHolderId));
                        }
                    },
                    getMenu: function (target) {
                        if (target.find('> ul > li').length) {
                            var menuItem = $('<ul />');
                            var item = this;
                            target.find('> ul > li').each(function () {
                                var txt = $(this).find(' > a').removeAttr('class').removeAttr('id'),
                                    hMenu = item.getMenu($(this));
                                $('<li />').append(txt).append(hMenu).appendTo(menuItem);
                            });

                            return menuItem;
                        }
                        return '';
                    },
                    loadMenu: function () {
                        // get browser width
                        currentWidth = window.innerWidth || document.documentElement.clientWidth;

                        if (!is_mobile) {
                            this.resetMenu();
                            if (currentWidth <= screenWidth && this.rtMenuFlag === false) {
                                console.log(this);
                                this.createMenu();
                            }
                        } else {
                            if (currentWidth <= screenWidth) {
                                if (rtMenuFlag === false) {
                                    this.createMenu();
                                }
                            } else {
                                this.resetMenu();
                            }

                        }
                    }
                }

                $(window).on('resize', function () {
                    obj.loadMenu();
                });

                $(function () {
                    obj.loadMenu();
                });

            });
        }

        return this.init();

        console.log(currentWidth);

    };

})(jQuery)
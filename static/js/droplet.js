var droplet = $("#droplet");
var topDroplet = $("#top-droplet");
var container = $("#droplet-container");
var stripe = $("#stripe");
var dropletInput = $("#droplet-input");

var pointerDown = function (e) {
    if (droplet.hasClass("animation-out")) {
        droplet.removeClass("animation-out");
        droplet.addClass("animation-in");
        topDroplet.removeClass("animation-out");
        topDroplet.addClass("animation-in");
    } else {
        droplet.addClass("animation-in");
        topDroplet.addClass("animation-in");
    }

    $(document).on("touchmove", pointerMove);
    $(document).on("mousemove", pointerMove)

    $(document).on("touchend", pointerUp);
    $(document).on("mouseup", pointerUp);
};

var pointerMove = function (e) {
    if ('ontouchstart' in document.documentElement) {
        var dropletX = e.originalEvent.touches[0].pageX - container.offset().left;
    } else {
        var dropletX = e.pageX - container.offset().left;
    }

    dropletX -= droplet.width() / 2;
    var minX = -droplet.width() / 2;
    var maxX = container.width() - droplet.width() / 2;

    if (dropletX <= minX) {
        dropletX = minX;
    }
    if (dropletX >= maxX) {
        dropletX = maxX;
    }

    var fillPercent = (dropletX + droplet.width() / 2) * 100 / (maxX - minX);
    var inputValue = Math.round(fillPercent);
    setDropletValue(inputValue);
};

var pointerUp = function () {
    app.level = parseInt(container.attr("data-value"));
    app.changeLevel();
    droplet.addClass("animation-out");
    droplet.removeClass("animation-in");
    topDroplet.addClass("animation-out");
    topDroplet.removeClass("animation-in");
    $(document).unbind("mousemove");
    $(document).unbind("touchmove");
    $(document).unbind("mouseup");
    $(document).unbind("touchend");
}

droplet.on("touchstart", pointerDown);
droplet.on("mousedown", pointerDown);

var getDropletValue = function () {
    return parseInt(container.attr("data-value"));
}

var setDropletValue = function (value) {
    container.attr("data-value", value);
    dropletInput.val(value);
    topDroplet.children(".value").text(value);
    stripe.css({
        width: value + "%"
    });

    var dropletLeft = container.width() * value / 100;
    dropletLeft -= droplet.width() / 2;
    droplet.css({
        left: dropletLeft
    });
    topDroplet.css({
        left: dropletLeft
    });
}
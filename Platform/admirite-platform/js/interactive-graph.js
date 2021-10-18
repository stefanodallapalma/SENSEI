colors = {
    blue: 'rgb(33, 150, 243)',
    purple: 'rgb(156, 39, 176)',
    yellow: 'rgb(255, 235, 59)',
    green: 'rgb(76, 175, 80)',
    red: 'rgb(244, 67, 54)',
    orange: 'rgb(255, 152, 0)',
    deep_orange: 'rgb(255, 87, 34)',
    blue_grey: 'rgb(96, 125, 139)',
    indigo: 'rgb(63, 81, 181)'
};

//capitalize only the first letter of the string. 
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function apiGetNProducts() {
    var res = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/market/n-products/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("N. Products for each market");
            console.log(data);
            res = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return res;
}

function getMarketGraph() {
    var res = null;

    $.ajax({
        url: 'http://0.0.0.0:4500/market/graph/',
        type: 'GET',
        datatype: 'jsonp',
        success: function(data) {
            console.log("Graph");
            console.log(data);
            res = data;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("ERROR")
            console.log(jqXHR.status)
            console.log(textStatus)
            console.log(errorThrown)
        },
        async: false
    });

    return res;
}

function getVendorGraphInfo(vendor) {
    var res = null;

    if (vendor != null) {
        var params = { "vendor-name": vendor }

        $.ajax({
            url: 'http://0.0.0.0:4500/market/graph/vendor',
            type: 'GET',
            data: params,
            datatype: 'jsonp',
            success: function(data) {
                console.log("Graph");
                console.log(data);
                res = data;
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("ERROR")
                console.log(jqXHR.status)
                console.log(textStatus)
                console.log(errorThrown)
            },
            async: false
        });
    }

    return res;
}

function initGraphData(data) {
    var links = []
    $.each(data, function(market, vendorList) {
        $.each(vendorList, function(idx, vendor) {
            links.push({ source: market, target: vendor })
        });
    });

    return links;
}

function initInteractiveGraph(links, parent_id, width = null, height = 600) {
    var nodes = {};

    // Compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = { name: link.source });
        link.target = nodes[link.target] || (nodes[link.target] = { name: link.target });
    });

    if (width == null) {
        var parentDiv = document.getElementById(parent_id);
        width = parentDiv.clientWidth;
    }

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(30)
        .charge(-300)
        .on("tick", tick)
        .start();

    var svg = d3.select("#" + parent_id).append("svg")
        .attr("width", width)
        .attr("height", height);

    var link = svg.selectAll(".link")
        .data(force.links())
        .enter().append("line")
        .attr("class", "link");

    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("click", mouseClick)
        .call(force.drag);

    node.append("circle")
        .attr("r", 8);

    node.append("text")
        .attr("x", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });

}

function addInfoToHtml(title, value, maxValue, subCaption = "", top = false) {
    title = title.replaceAll("/", "-");
    title = title.replaceAll(" ", "-");

    var mTop = "mT-15"
    if (top == true) {
        mTop = "mT-25"
    }

    if (subCaption != null && subCaption != "") {
        subCaption += ": "
    }

    var div = '<div class="layer w-100 ' + mTop + '">\
    <h5 id="' + title + '" class="mB-5">' + capitalizeFirstLetter(title.replaceAll("-", " ")) + '</h5>\
    <small id="' + title + '" class="fw-600 c-grey-700">' + subCaption + value + '</small>\
    <span id="' + title + '-percentage" class="pull-right c-grey-600 fsz-sm"></span>\
    <div class="progress mT-10">\
    <div id="' + title + '-percentage-bar" class="progress-bar bgc-deep-purple-500" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"><span class="sr-only">50% Complete</span></div>\
    </div></div>'

    $('#vendor_info').append(div);

    var percentage = ((value / maxValue) * 100).toFixed(2);
    $('#' + title + '-percentage').text(percentage + "%");
    $('#' + title + '-percentage-bar').attr('aria-valuenow', "" + percentage);
    $('#' + title + '-percentage-bar').css('width', percentage + "%");
}

(function($) {
    $.fn.invisible = function() {
        return this.each(function() {
            $(this).css("visibility", "hidden");
        });
    };
    $.fn.visible = function() {
        return this.each(function() {
            $(this).css("visibility", "visible");
        });
    };
}(jQuery));


$('#vendor_info_container').invisible();

var data = getMarketGraph();
links = initGraphData(data);
var n_markets = Object.keys(data).length;
var market_nproducts = apiGetNProducts();

var nodes = {};

// Compute the distinct nodes from the links.
links.forEach(function(link) {
    link.source = nodes[link.source] || (nodes[link.source] = { name: link.source });
    link.target = nodes[link.target] || (nodes[link.target] = { name: link.target });
});

var parentDiv = document.getElementById("graph-container");
var width = parentDiv.clientWidth;

var height = 600;

var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .linkDistance(30)
    .charge(-300)
    .on("tick", tick)
    .start();

var svg = d3.select("#graph-container").append("svg")
    .attr("width", width)
    .attr("height", height);

var link = svg.selectAll(".link")
    .data(force.links())
    .enter().append("line")
    .attr("class", "link");

var node = svg.selectAll(".node")
    .data(force.nodes())
    .enter().append("g")
    .attr("class", "node")
    .on("mouseover", mouseover)
    .on("mouseout", mouseout)
    .on("click", mouseClick)
    .call(force.drag);

node.append("circle")
    .attr("r", 8);

node.append("text")
    .attr("x", 12)
    .attr("dy", ".35em")
    .text(function(d) { return d.name; });

function tick() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}

function mouseover() {
    d3.select(this).select("circle").transition()
        .duration(750)
        .attr("r", 16);
}

function mouseout() {
    d3.select(this).select("circle").transition()
        .duration(750)
        .attr("r", 8);
}

function mouseClick() {
    var label = d3.select(this).text();
    console.log(label);
    if (data.hasOwnProperty(label)) {
        console.log("Node: MARKET");
        $('#vendor_info').empty();
        $('#vendor_info_container').invisible();
    } else {
        console.log("Node: VENDOR");
        var vendor_info = getVendorGraphInfo(label);

        $('#vendor_info').empty();

        $('#vendor_info').append('<h6 class="ta-c">' + vendor_info["vendor"] + '</h6>'); // Name
        addInfoToHtml("Number of Markets", vendor_info["n_markets"], n_markets, subCaption = "# of markets", top = true); // N. Markets

        if (vendor_info["markets"] == null) {
            addInfoToHtml("Products", 0, 1, subCaption = "# of products");
        } else {
            $('#vendor_info').append('<h5 class="bdB mT-30 mB-10">Products</h5>');
            $.each(vendor_info["markets"], function(key, value) {
                addInfoToHtml(key, value, market_nproducts[key], subCaption = "# of products");
            });
        }

        $('#vendor_info_container').visible();
    }
}
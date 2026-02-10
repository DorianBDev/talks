#!/usr/bin/env python3

# Indexer v.1.0.1
# Author: Josh Brunty (josh dot brunty at marshall dot edu)

# This is a modified version of Josh's work

import datetime
import os
from pathlib import Path
from urllib.parse import quote

DEFAULT_OUTPUT_FILE = "index.html"

EXCLUDE_DIR = [".github", ".git"]
EXCLUDE_FILES = ["index.html", "open-dir.py", ".gitattributes"]


def process_dir(top_dir):
    glob_patt = "*"

    path_top_dir: Path
    path_top_dir = Path(top_dir)
    index_file = None

    index_path = Path(path_top_dir, "index.html")

    if index_path.exists():
        return

    try:
        index_file = open(index_path, "w", encoding="utf-8")
    except Exception as e:
        print("cannot create file %s %s" % (index_path, e))
        return

    path_top_dir_parents = path_top_dir.parents
    path_format = "/ <a style='text-decoration: underline;' href='https://dorianb.net/talks/'>Talks</a> "
    for parent in reversed(path_top_dir_parents):
        if parent.name != "":
            path_format += f"/<a style='text-decoration: underline;' href='https://dorianb.net/talks/{parent}'>{parent.name}</a>"
    path_format += f"/<a style='text-decoration: underline;' href='https://dorianb.net/talks/{path_top_dir}'>{path_top_dir.name}</a>"

    index_file.write(
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dorian B. Talks</title>
    <style>
    * { padding: 0; margin: 0; }
    body {
        font-family: sans-serif;
        text-rendering: optimizespeed;
        background-color: #000000;
        color: #ffffff;
    }
    a {
        color: #00ffff;
        text-decoration: none;
    }
    a:hover,
    h1 a:hover {
        color: #ffffff;
    }
    header,
    #summary {
        padding-left: 5%;
        padding-right: 5%;
    }
    th:first-child,
    td:first-child {
        width: 5%;
    }
    th:last-child,
    td:last-child {
        width: 5%;
    }
    header {
        padding-top: 25px;
        padding-bottom: 15px;
    }
    h1 {
        font-size: 20px;
        font-weight: normal;
        white-space: nowrap;
        overflow-x: hidden;
        text-overflow: ellipsis;
        color: #ffffff;
    }
    h1 a {
        color: #ffffff;
        margin: 0 4px;
    }
    h1 a:hover {
        text-decoration: underline;
    }
    h1 a:first-child {
        margin: 0;
    }
    main {
        display: block;
    }
    .meta {
        font-size: 12px;
        font-family: Verdana, sans-serif;
        border-bottom: 1px solid #9C9C9C;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .meta-item {
        margin-right: 1em;
    }
    #filter {
        padding: 4px;
        border: 1px solid #CCC;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    tr {
        border-bottom: 1px dashed #4a4a4a;
    }
    tbody tr:hover {
        background-color: #111111;
    }
    th,
    td {
        text-align: left;
        padding: 10px 0;
    }
    th {
        padding-top: 15px;
        padding-bottom: 15px;
        font-size: 16px;
        white-space: nowrap;
    }
    th a {
        color: black;
    }
    th svg {
        vertical-align: middle;
    }
    td {
        white-space: nowrap;
        font-size: 14px;
    }
    td:nth-child(2) {
        width: 80%;
    }
    th:nth-child(3) {
        text-align: center;
    }
    th:nth-child(4) {
        text-align: center;
    }
    td:nth-child(3) {
        padding: 0 20px 0 20px;
        text-align: center;
    }
    td:nth-child(4) {
        padding: 0 20px 0 20px;
        text-align: center;
    }
    th:nth-child(5),
    td:nth-child(5) {
    }
    td:nth-child(2) svg {
        position: absolute;
    }
    td .name {
        margin-left: 1.75em;
        word-break: break-all;
        overflow-wrap: break-word;
        white-space: pre-wrap;
    }
    td .goup {
        margin-left: 1.75em;
        padding: 0;
        word-break: break-all;
        overflow-wrap: break-word;
        white-space: pre-wrap;
    }
    .icon {
        margin-right: 5px;
    }
    tr.clickable { 
        cursor: pointer; 
    } 
    tr.clickable a { 
        display: block; 
    } 
    @media (max-width: 600px) {
        .hideable {
            display: none;
        }
        td:nth-child(2) {
            width: auto;
        }
        th:nth-child(3),
        td:nth-child(3) {
            padding-right: 5%;
            text-align: right;
        }
        h1 {
            color: #ffffff;
        }
        h1 a {
            margin: 0;
        }
        #filter {
            max-width: 100px;
        }
    }
    </style>
</head>


<body>
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="0" width="0" style="position: absolute;">
    <defs>
        <!-- Go-up -->
        <g id="go-up">
            <path d="M10,9V5L3,12L10,19V14.9C15,14.9 18.5,16.5 21,20C20,15 17,10 10,9Z" fill="#696969"/>
        </g>
        <!-- Folder -->
        <g id="folder" fill-rule="nonzero" fill="none">
            <path d="M285.22 37.55h-142.6L110.9 0H31.7C14.25 0 0 16.9 0 37.55v75.1h316.92V75.1c0-20.65-14.26-37.55-31.7-37.55z" fill="#FFA000"/>
            <path d="M285.22 36H31.7C14.25 36 0 50.28 0 67.74v158.7c0 17.47 14.26 31.75 31.7 31.75H285.2c17.44 0 31.7-14.3 31.7-31.75V67.75c0-17.47-14.26-31.75-31.7-31.75z" fill="#FFCA28"/>
        </g>
        <g id="folder-shortcut" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="folder-shortcut-group" fill-rule="nonzero">
                <g id="folder-shortcut-shape">
                    <path d="M285.224876,37.5486902 L142.612438,37.5486902 L110.920785,0 L31.6916529,0 C14.2612438,0 0,16.8969106 0,37.5486902 L0,112.646071 L316.916529,112.646071 L316.916529,75.0973805 C316.916529,54.4456008 302.655285,37.5486902 285.224876,37.5486902 Z" id="Shape" fill="#FFA000"></path>
                    <path d="M285.224876,36 L31.6916529,36 C14.2612438,36 0,50.2838568 0,67.7419039 L0,226.451424 C0,243.909471 14.2612438,258.193328 31.6916529,258.193328 L285.224876,258.193328 C302.655285,258.193328 316.916529,243.909471 316.916529,226.451424 L316.916529,67.7419039 C316.916529,50.2838568 302.655285,36 285.224876,36 Z" id="Shape" fill="#FFCA28"></path>
                </g>
                <path d="M126.154134,250.559184 C126.850974,251.883673 127.300549,253.006122 127.772602,254.106122 C128.469442,255.206122 128.919016,256.104082 129.638335,257.002041 C130.559962,258.326531 131.728855,259 133.100057,259 C134.493737,259 135.415364,258.55102 136.112204,257.67551 C136.809044,257.002041 137.258619,255.902041 137.258619,254.577551 C137.258619,253.904082 137.258619,252.804082 137.033832,251.457143 C136.786566,249.908163 136.561779,249.032653 136.561779,248.583673 C136.089726,242.814286 135.864939,237.920408 135.864939,233.273469 C135.864939,225.057143 136.786566,217.514286 138.180246,210.846939 C139.798713,204.202041 141.889234,198.634694 144.429328,193.763265 C147.216689,188.869388 150.678411,184.873469 154.836973,181.326531 C158.995535,177.779592 163.626149,174.883673 168.481552,172.661224 C173.336954,170.438776 179.113983,168.665306 185.587852,167.340816 C192.061722,166.218367 198.760378,165.342857 205.481514,164.669388 C212.18017,164.220408 219.598146,163.995918 228.162535,163.995918 L246.055591,163.995918 L246.055591,195.514286 C246.055591,197.736735 246.752431,199.510204 248.370899,201.059184 C250.214153,202.608163 252.079886,203.506122 254.372715,203.506122 C256.463236,203.506122 258.531277,202.608163 260.172223,201.059184 L326.102289,137.797959 C327.720757,136.24898 328.642384,134.47551 328.642384,132.253061 C328.642384,130.030612 327.720757,128.257143 326.102289,126.708163 L260.172223,63.4469388 C258.553756,61.8979592 256.463236,61 254.395194,61 C252.079886,61 250.236632,61.8979592 248.393377,63.4469388 C246.77491,64.9959184 246.07807,66.7693878 246.07807,68.9918367 L246.07807,100.510204 L228.162535,100.510204 C166.863084,100.510204 129.166282,117.167347 115.274437,150.459184 C110.666301,161.54898 108.350993,175.310204 108.350993,191.742857 C108.350993,205.279592 113.903236,223.912245 124.760454,247.438776 C125.00772,248.112245 125.457294,249.010204 126.154134,250.559184 Z" id="Shape" fill="#FFFFFF" transform="translate(218.496689, 160.000000) scale(-1, 1) translate(-218.496689, -160.000000) "></path>
            </g>
        </g>
        <!-- File -->
        <g id="file" stroke="#000" stroke-width="25" fill="#FFF" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 24.12v274.76c0 6.16 5.87 11.12 13.17 11.12H239c7.3 0 13.17-4.96 13.17-11.12V136.15S132.6 13 128.37 13H26.17C18.87 13 13 17.96 13 24.12z"/>
            <path d="M129.37 13L129 113.9c0 10.58 7.26 19.1 16.27 19.1H249L129.37 13z"/>
        </g>
        <g id="file-shortcut" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
            <g id="file-shortcut-group" transform="translate(13.000000, 13.000000)">
                <g id="file-shortcut-shape" stroke="#000000" stroke-width="25" fill="#FFFFFF" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M0,11.1214886 L0,285.878477 C0,292.039924 5.87498876,296.999983 13.1728373,296.999983 L225.997983,296.999983 C233.295974,296.999983 239.17082,292.039942 239.17082,285.878477 L239.17082,123.145388 C239.17082,123.145388 119.58541,2.84217094e-14 115.369423,2.84217094e-14 L13.1728576,2.84217094e-14 C5.87500907,-1.71479982e-05 0,4.96022995 0,11.1214886 Z" id="rect1171"></path>
                    <path d="M116.37005,0 L116,100.904964 C116,111.483663 123.258008,120 132.273377,120 L236,120 L116.37005,0 L116.37005,0 Z" id="rect1794"></path>
                </g>
                <path d="M47.803141,294.093878 C48.4999811,295.177551 48.9495553,296.095918 49.4216083,296.995918 C50.1184484,297.895918 50.5680227,298.630612 51.2873415,299.365306 C52.2089688,300.44898 53.3778619,301 54.7490634,301 C56.1427436,301 57.0643709,300.632653 57.761211,299.916327 C58.4580511,299.365306 58.9076254,298.465306 58.9076254,297.381633 C58.9076254,296.830612 58.9076254,295.930612 58.6828382,294.828571 C58.4355724,293.561224 58.2107852,292.844898 58.2107852,292.477551 C57.7387323,287.757143 57.5139451,283.753061 57.5139451,279.95102 C57.5139451,273.228571 58.4355724,267.057143 59.8292526,261.602041 C61.44772,256.165306 63.5382403,251.610204 66.0783349,247.62449 C68.8656954,243.620408 72.3274172,240.35102 76.4859792,237.44898 C80.6445412,234.546939 85.2751561,232.177551 90.1305582,230.359184 C94.9859603,228.540816 100.76299,227.089796 107.236859,226.006122 C113.710728,225.087755 120.409385,224.371429 127.13052,223.820408 C133.829177,223.453061 141.247152,223.269388 149.811542,223.269388 L167.704598,223.269388 L167.704598,249.057143 C167.704598,250.87551 168.401438,252.326531 170.019905,253.593878 C171.86316,254.861224 173.728893,255.595918 176.021722,255.595918 C178.112242,255.595918 180.180284,254.861224 181.82123,253.593878 L247.751296,201.834694 C249.369763,200.567347 250.291391,199.116327 250.291391,197.297959 C250.291391,195.479592 249.369763,194.028571 247.751296,192.761224 L181.82123,141.002041 C180.202763,139.734694 178.112242,139 176.044201,139 C173.728893,139 171.885639,139.734694 170.042384,141.002041 C168.423917,142.269388 167.727077,143.720408 167.727077,145.538776 L167.727077,171.326531 L149.811542,171.326531 C88.5120908,171.326531 50.8152886,184.955102 36.9234437,212.193878 C32.3153075,221.267347 30,232.526531 30,245.971429 C30,257.046939 35.5522422,272.291837 46.4094607,291.540816 C46.6567266,292.091837 47.1063009,292.826531 47.803141,294.093878 Z" id="Shape-Copy" fill="#000000" fill-rule="nonzero" transform="translate(140.145695, 220.000000) scale(-1, 1) translate(-140.145695, -220.000000) "></path>
            </g>
        </g>
        <!-- Gitub -->
        <g id="github">
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" fill="#696969"/>
        </g>
    </defs>
    </svg>

<style>
    .navigation-bar {
        margin-top: 20px;
        margin-right: 8px;
        font-family: "Droid Sans", Arial, Helvetica, sans-serif;
        font-size: 16px;
        font-weight: 700;
        line-height: 18.4px;
    }

    .navigation-bar ul {
        cursor: default;
        list-style: none;
        padding: 0px;
        margin: 0px;
        justify-content: right;
        display: flex;
        overflow-x: visible;
    }

    .navigation-bar li {
        margin-right: 0px;
    }

    .navigation-bar li.icon a {
        display: block;
        padding: 10px;
        border: 2px solid grey;
        border-radius: 0px;
        margin-right: -2px;
        display: inline;
        float: left;
        justify-content: center;
        font-weight: bold;
        color: white;
    }

    .navigation-bar li.icon a:hover {
        background-color: grey;
    }

    .navigation-bar li.icon a span {
        margin-right: 5px;
        padding: 0px;
    }
</style>

<link
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css"
    rel="stylesheet"
    type="text/css"
/>

<!-- Navigation -->
<div class="navigation-bar">
  <!-- Navigation -->
  <ul>
    <!-- Home -->
    <li class="icon">
      <a href="https://dorianb.net">
        <span class="fa fa-home"></span>
        Home
      </a>
    </li>

    <!-- Blog -->
    <li class="icon">
      <a href="https://dorianb.net/blog">
        <span class="fa fa-book"></span>
        Blog
      </a>
    </li>

    <!-- Talks -->
    <li class="icon">
      <a href="https://dorianb.net/talks">
        <span class="fa fa-solid fa-comment"></span>
        Talks
      </a>
    </li>
  </ul>
</div>


<style>
    .star{display: block; background-color: #fff; position: absolute; border-radius: 100%; animation-timing-function: linear; animation-iteration-count: infinite;}

    @keyframes move_right {
       from { transform: rotate(0deg) translateX(8px) rotate(0deg); }
        to   { transform: rotate(360deg) translateX(8px) rotate(-360deg); }
    }

    @keyframes move_left {
       from { transform: rotate(0deg) translateX(8px) rotate(0deg); }
        to   { transform: rotate(-360deg) translateX(8px) rotate(360deg); }
    }
</style>

<script>
    /**
     * Generates a random number between a given range (min and max).
     * @param {number} min - The minimum value for the random number.
     * @param {number} max - The maximum value for the random number.
     * @return {number} A random number between min and max (inclusive).
     */
    var randomNumber = function(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    };

    /**
     * Holds the number of stars to be created.
     */
    var numberOfStars = randomNumber(50, 350);

    /**
     * Creates stars with random positions, sizes, and animation directions.
     */
    var createStars = function() {
        /**
         * Holds the initial star rotation direction.
         */
        var starRotation = 'move_right;';

        var body = document.body,
            html = document.documentElement;

        var height = Math.max(body.scrollHeight, body.offsetHeight, 
                              html.clientHeight, html.scrollHeight, html.offsetHeight);

        // Loop through the number of stars to be created
        var stars = "";
        for (var i = 0; i < numberOfStars; i++) {
            // Switch the rotation direction for each star
            var rotation = (starRotation === 'move_right;' ? 'move_left;' : 'move_right;');

            // Generate random values for star's position, size, and animation duration
            var starTop = randomNumber(0, height);
                var starLeft = randomNumber(0, window.innerWidth);
                var starRadius = randomNumber(0, 4);
                var starDuration = randomNumber(6, 16);

                // Create a new star with the generated values and add it to the body of the document
                stars += "<div class='star' style='top: " + starTop + "px; left: " + starLeft + "px; width: " + starRadius + "px; height: " + starRadius + "px; " +
                    "animation-name:" + rotation + "; animation-duration: " + starDuration + "s;z-index: -1;'></div>";
            }
            document.body.innerHTML += "<div id='stars'>" + stars + "</div>";
        };

        // Create stars
        createStars();    
    </script>

    <script>
	// ============================================================================
	// Configuration
	// ============================================================================

	const GRADIENTS = {
	  poly1: {
	    from: '#0e3158',
	    to: '#091144',
	    direction: 'to right',
	  },
	  poly2: {
	    from: '#154984',
	    to: '#060b2d',
	    direction: 'to left',
	  },
	  poly3: {
	    from: '#002b33',
	    to: '#007380',
	    direction: 'to top',
	    opacity: 0.2,
	  },
	};

	const POLYGON_COUNTS = {
	  poly1: 10,
	  poly2: 6,
	  poly3: 3,
	};

	const DISTRIBUTION_SETTINGS = {
	  overflow: 0.3,
	  disturb: 0.3,
	  disturbChance: 0.3,
	};

	const ANIMATION = {
	  blur: 70, // px
	  transitionDuration: 3.5, // seconds
	};

	// ============================================================================
	// Configuration (can be modified)
	// ============================================================================

	let config = {
	  distribution: 'full',
	  opacity: 0.2,
	  hue: 0,
	};

	// ============================================================================
	// Distribution Logic
	// ============================================================================

	function distributionToLimits(distribution) {
	  const min = -0.2;
	  const max = 1.2;
	  let x = [min, max];
	  let y = [min, max];

	  const intersection = (a, b) => [
	    Math.max(a[0], b[0]),
	    Math.min(a[1], b[1]),
	  ];

	  const limits = distribution.split('-');

	  const limitHandlers = {
	    topmost: () => { y = intersection(y, [-0.5, 0]); },
	    top: () => { y = intersection(y, [min, 0.6]); },
	    bottom: () => { y = intersection(y, [0.4, max]); },
	    left: () => { x = intersection(x, [min, 0.6]); },
	    right: () => { x = intersection(x, [0.4, max]); },
	    xcenter: () => { x = intersection(x, [0.25, 0.75]); },
	    ycenter: () => { y = intersection(y, [0.25, 0.75]); },
	    center: () => {
	      x = intersection(x, [0.25, 0.75]);
	      y = intersection(y, [0.25, 0.75]);
	    },
	    full: () => {
	      x = intersection(x, [0, 1]);
	      y = intersection(y, [0, 1]);
	    },
	  };

	  for (const limit of limits) {
	    if (limitHandlers[limit]) {
	      limitHandlers[limit]();
	    }
	  }

	  return { x, y };
	}

	// ============================================================================
	// Polygon Generation
	// ============================================================================

	function distance2([x1, y1], [x2, y2]) {
	  return (x2 - x1) ** 2 + (y2 - y1) ** 2;
	}

	class Polygon {
	  constructor(count, gradientKey) {
	    this.count = count;
	    this.gradientKey = gradientKey;
	    this.points = [];
	    this.element = null;
	    this.generatePoints();
	  }

	  generatePoints() {
	    const limits = distributionToLimits(config.distribution);
	    const { overflow, disturb, disturbChance } = DISTRIBUTION_SETTINGS;

	    const randomBetween = ([a, b]) => Math.random() * (b - a) + a;

	    const applyOverflow = (random, overflow) => {
	      random = random * (1 + overflow * 2) - overflow;
	      return Math.random() < disturbChance ? random + (Math.random() - 0.5) * disturb : random;
	    };

	    const newPoints = Array.from({ length: this.count }, () => [
	      applyOverflow(randomBetween(limits.x), overflow),
	      applyOverflow(randomBetween(limits.y), overflow),
	    ]);

	    if (this.points.length === 0) {
	      this.points = newPoints;
	    } else {
	      const availableNewPoints = new Set(newPoints);
	      this.points = this.points.map((oldPoint) => {
	        let minDistance = Infinity;
	        let closest = null;

	        for (const newPoint of availableNewPoints) {
	          const d = distance2(oldPoint, newPoint);
	          if (d < minDistance) {
	            minDistance = d;
	            closest = newPoint;
	          }
	        }

	        if (closest) availableNewPoints.delete(closest);
	        return closest || oldPoint;
	      });
	    }
	  }

	  getPolygonString() {
	    return this.points
	      .map(([x, y]) => `${x * 100}% ${y * 100}%`)
	      .join(', ');
	  }

	  createElement() {
	    const div = document.createElement('div');
	    div.className = 'glow-clip';
	    div.id = 'glow-' + this.gradientKey;
	    this.element = div;
	    return div;
	  }

	  updateStyle() {
	    if (!this.element) return;
    
	    const gradient = GRADIENTS[this.gradientKey];
	    const opacity = gradient.opacity !== undefined ? gradient.opacity : config.opacity;
    
	    this.element.style.clipPath = `polygon(${this.getPolygonString()})`;
	    this.element.style.opacity = opacity;
	    this.element.style.background = `linear-gradient(${gradient.direction}, ${gradient.from}, ${gradient.to})`;
	  }

	  regenerate() {
	    this.generatePoints();
	  }
	}

	// ============================================================================
	// Helper Functions
	// ============================================================================

	function getFullPageHeight() {
	  const body = document.body;
	  const html = document.documentElement;
	  return Math.max(
	    body.scrollHeight, body.offsetHeight,
	    html.clientHeight, html.scrollHeight, html.offsetHeight
	  );
	}

	// ============================================================================
	// Initialize and Create DOM Elements
	// ============================================================================

	var createGlowEffect = function() {
	  // Create main container with absolute positioning
	  const container = document.createElement('div');
	  container.id = 'glow-container';
  
	  function updateContainerHeight() {
	    const pageHeight = getFullPageHeight();
	    container.style.cssText = `
	      position: absolute;
	      top: 0;
	      left: 0;
	      width: 100%;
	      height: ${pageHeight}px;
	      z-index: -1;
	      overflow: hidden;
	      pointer-events: none;
	    `;
	  }

	  // Set initial height
	  updateContainerHeight();

	  // Create background wrapper
	  const bgWrapper = document.createElement('div');
	  bgWrapper.id = 'glow-bg-effect';
	  bgWrapper.className = 'glow-bg';
	  bgWrapper.setAttribute('aria-hidden', 'true');
	  bgWrapper.style.cssText = `
	    width: 100%;
	    height: 100%;
	    position: relative;
	  `;

	  // Add style for glow-clip elements
	  const style = document.createElement('style');
	  style.textContent = `
	    .glow-clip {
	      position: absolute;
	      width: 100%;
	      height: 100%;
	      transition: clip-path ${ANIMATION.transitionDuration}s ease-in-out, 
	                  opacity ${ANIMATION.transitionDuration}s ease-in-out;
	    }
	  `;
	  document.head.appendChild(style);

	  // Create polygons
	  const polygons = {
	    poly1: new Polygon(POLYGON_COUNTS.poly1, 'poly1'),
	    poly2: new Polygon(POLYGON_COUNTS.poly2, 'poly2'),
	    poly3: new Polygon(POLYGON_COUNTS.poly3, 'poly3'),
	  };

	  // Create and append polygon elements
	  Object.values(polygons).forEach(poly => {
	    bgWrapper.appendChild(poly.createElement());
	  });

	  // Append to container
	  container.appendChild(bgWrapper);

	  // Append to body
	  document.body.appendChild(container);

	  // Update all styles
	  function updateAllPolygons() {
	    Object.values(polygons).forEach(poly => poly.updateStyle());
	    bgWrapper.style.filter = `blur(${ANIMATION.blur}px) hue-rotate(${config.hue}deg)`;
	  }

	  function regeneratePolygons() {
	    Object.values(polygons).forEach(poly => poly.regenerate());
	    updateAllPolygons();
	  }

	  // Initial render
	  updateAllPolygons();

	  // Update height on window resize and content changes
	  window.addEventListener('resize', updateContainerHeight);
  
	  // Use ResizeObserver to detect content height changes
	  if (typeof ResizeObserver !== 'undefined') {
	    const resizeObserver = new ResizeObserver(() => {
	      updateContainerHeight();
	    });
	    resizeObserver.observe(document.body);
	  }

	  // Fallback: periodically check for height changes
	  setInterval(updateContainerHeight, 1000);

	  // ============================================================================
	  // Public API
	  // ============================================================================

	  window.glowEffect = {
	    setDistribution(distribution) {
	      config.distribution = distribution;
	      regeneratePolygons();
	    },
	    setOpacity(opacity) {
	      config.opacity = opacity;
	      updateAllPolygons();
	    },
	    setHue(hue) {
	      config.hue = hue;
	      updateAllPolygons();
	    },
	    regenerate() {
	      regeneratePolygons();
	    },
	    updateHeight() {
	      updateContainerHeight();
	    },
	    startAutoRegenerate(interval = 5000) {
	      this.autoRegenerateInterval = setInterval(() => {
	        regeneratePolygons();
	      }, interval);
	    },
	    stopAutoRegenerate() {
	      if (this.autoRegenerateInterval) {
	        clearInterval(this.autoRegenerateInterval);
	      }
	    }
	  };
	};

	createGlowEffect();
	</script>
      
<header>
    <h1>"""
        f"<a href='https://github.com/DorianBDev/talks/tree/main/'><svg width='1.5em' height='1em' version='1.1' viewBox='5 0 24 24'><use xlink:href='#github'></use></svg></a> {path_format}"
        f"""</h1>
                 </header>
                 <main>
                 <div class="listing">
                     <table aria-describedby="summary">
                         <thead>
                         <tr>
                             <th></th>
                             <th>Name</th>
                             <th>Links</th>
                             <th>Size</th>
                             <th>Modified</th>
                             <th></th>
                         </tr>
                         </thead>
                         <tbody>
                         <tr class="clickable">
                             <td></td>
                             <td><a href=".."><svg width="1.5em" height="1em" version="1.1" viewBox="0 0 24 24"><use xlink:href="#go-up"></use></svg>
                 <span class="goup">..</span></a></td>
                             <td><a href="https://github.com/DorianBDev/talks/tree/main/{path_top_dir}"><svg width="1.5em" height="1em" version="1.1" viewBox="0 0 24 24"><use xlink:href="#github"></use></svg></a></td>
                             <td>&mdash;</td>
                             <td>&mdash;</td>
                             <td></td>
                         </tr>
                 """
    )

    # sort dirs first
    sorted_entries = sorted(
        path_top_dir.glob(glob_patt), key=lambda p: (p.is_file(), p.name)
    )

    entry: Path
    for entry in sorted_entries:

        if entry.is_dir() and entry.name.lower() not in EXCLUDE_DIR:
            print(f"{entry.name.lower()}")
            process_dir(entry)

        # don't include index.html in the file listing
        if entry.name.lower() in EXCLUDE_FILES or entry.name.lower() in EXCLUDE_DIR:
            print(f"{entry.name.lower()}")
            continue

        # From Python 3.6, os.access() accepts path-like objects
        if (not entry.is_symlink()) and not os.access(str(entry), os.W_OK):
            print(
                f"*** WARNING *** entry {entry.absolute()} is not writable! SKIPPING!"
            )
            continue

        size_bytes = -1  ## is a folder
        size_pretty = "&mdash;"
        last_modified = "-"
        last_modified_human_readable = "-"
        last_modified_iso = ""
        try:
            if entry.is_file():
                size_bytes = entry.stat().st_size
                size_pretty = pretty_size(size_bytes)

            if entry.is_dir() or entry.is_file():
                last_modified = datetime.datetime.fromtimestamp(
                    entry.stat().st_mtime
                ).replace(microsecond=0)
                last_modified_iso = last_modified.isoformat()
                last_modified_human_readable = last_modified.strftime("%c")

        except Exception as e:
            print("ERROR accessing file name:", e, entry)
            continue

        entry_path = str(entry.name)

        if entry.is_dir() and not entry.is_symlink():
            entry_type = "folder"
            if os.name not in ("nt",):
                # append trailing slash to dirs, unless it's windows
                entry_path = os.path.join(entry.name, "")

        elif entry.is_dir() and entry.is_symlink():
            entry_type = "folder-shortcut"
            print("dir-symlink", entry.absolute())

        elif entry.is_file() and entry.is_symlink():
            entry_type = "file-shortcut"
            print("file-symlink", entry.absolute())

        else:
            entry_type = "file"

        index_file.write(
            f"""
        <tr class="file">
            <td></td>
            <td>
                <a href="{quote(entry_path)}">
                    <svg width="1.5em" height="1em" version="1.1" viewBox="0 0 265 323"><use xlink:href="#{entry_type}"></use></svg>
                    <span class="name">{entry.name}</span>
                </a>
            </td>
            <td><a href="https://github.com/DorianBDev/talks/tree/main/{path_top_dir}/{entry_path}"><svg width="1.5em" height="1em" version="1.1" viewBox="0 0 24 24"><use xlink:href="#github"></use></svg></a></td>
            <td data-order="{size_bytes}">{size_pretty}</td>
            <td><time datetime="{last_modified_iso}">{last_modified_human_readable}</time></td>
            <td></td>
        </tr>
"""
        )

    index_file.write(
        """
            </tbody>
        </table>
    </div>
</main>
</body>
</html>"""
    )
    if index_file:
        index_file.close()


# bytes pretty-printing
UNITS_MAPPING = [
    (1024**5, " PB"),
    (1024**4, " TB"),
    (1024**3, " GB"),
    (1024**2, " MB"),
    (1024**1, " KB"),
    (1024**0, (" byte", " bytes")),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Human-readable file sizes.
    ripped from https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


if __name__ == "__main__":
    process_dir(".")

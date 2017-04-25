/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */

/*
 wger exercise functions
 */

'use strict';

/*
 Highlight a muscle in the overview
 */
function wgerHighlightMuscle(element) {
  var $muscle;
  var muscleId;
  var isFront;
  var divId;
  divId = $(element).data('target');
  isFront = ($(element).data('isFront') === 'True') ? 'front' : 'back';
  muscleId = divId.match(/\d+/);

  // Reset all other highlighted muscles
  $muscle = $('.muscle');
  $muscle.removeClass('muscle-hover');
  $muscle.addClass('muscle-not-inactive');

  // Highlight the current one
  $(element).removeClass('muscle-not-hover');
  $(element).addClass('muscle-hover');


  // Set the corresponding background
  $('#muscle-system').css('background-image',
    'url(/static/images/muscles/main/muscle-' + muscleId + '.svg),' +
    'url(/static/images/muscles/muscular_system_' + isFront + '.svg)');

    if (isFront === 'front') {
        $('#muscle-direction #set-front').hide();
        $('#muscle-direction #set-back').show();
        displaySVGMuscles('front');
    }
    else if (isFront === 'back'){
        $('#muscle-direction #set-back').hide();
        $('#muscle-direction #set-front').show();
        displaySVGMuscles('back')
    }
}

/*
 D3js functions
 */

function wgerDrawWeightLogChart(data, divId) {
  var chartData;
  var legend;
  var minValues;
  var i;
  if (data.length) {
    legend = [];
    minValues = [];
    chartData = [];
    for (i = 0; i < data.length; i++) {
      chartData[i] = MG.convert.date(data[i], 'date');

      // Read the possible repetitions for the chart legend
      legend[i] = data[i][0].reps;

      // Read the minimum values for each repetition
      minValues[i] = d3.min(data[i], function (repetitionData) {
        return repetitionData.weight;
      });
    }

    MG.data_graphic({
      data: chartData,
      y_accessor: 'weight',
      min_y: d3.min(minValues),
      aggregate_rollover: true,
      full_width: true,
      top: 10,
      left: 30,
      right: 10,
      height: 200,
      legend: legend,
      target: '#svg-' + divId,
      colors: ['#204a87', '#4e9a06', '#ce5c00', '#5c3566', '#2e3436', '#8f5902', '#a40000']
    });
  }
}

function wgerShowMuscleDetails(element){
    var divId = $(element).attr('class');
    var muscleId = divId.match(/\d+/)[0];
    var element2 = $('.muscle[data-target="muscle-' + muscleId + '"]')
    wgerHighlightMuscle(element2)

    // Add on click trigger
    $(element).click(function() {
        $(element2).click();
    });

}

function setMuscleDirection(orientation){
    if (orientation === 'front') {
        var muscles_orientation = $("#muscle-system").attr('style').match(/\(\w+muscular_system_back.svg/);
        // Set the corresponding background
        $('#muscle-system').css('background-image',
            'url(/static/images/muscles/muscular_system_front.svg)');
        displaySVGMuscles('front');
        console.log("dir front: ", muscles_orientation);
    }
    else if (orientation === 'back') {
        var muscles_orientation = $("#muscle-system").attr('style').match(/\(\w+muscular_system_back.svg/);
        $('#muscle-system').css('background-image',
            'url(/static/images/muscles/muscular_system_back.svg)');
        displaySVGMuscles('back');
        console.log("dir back: ", muscles_orientation)
    }
}

function displaySVGMuscles(orientation) {
    if (orientation === 'front') {
        $('.muscle-svg.back-muscle').hide();
        $('.muscle-svg.front-muscle').show();
    } else if (orientation === 'back') {
        $('.muscle-svg.front-muscle').hide();
        $('.muscle-svg.back-muscle').show();
    }
}


$(document).ready(function (){
    var path =  $('svg path');
    path.hover(function() {
        wgerShowMuscleDetails(this);
    });

    path.click(function() {
        wgerShowMuscleDetails(this);
    });

    $('#muscle-direction #set-front').click(function(){
        setMuscleDirection('front');
        $('#muscle-direction #set-front').hide();
        $('#muscle-direction #set-back').show();
    });
    $('#muscle-direction #set-back').click(function() {
        setMuscleDirection('back');
        $('#muscle-direction #set-back').hide();
        $('#muscle-direction #set-front').show();

    });
});

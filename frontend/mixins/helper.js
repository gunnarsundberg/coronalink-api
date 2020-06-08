/* Collection of helper functions */

/* Adds commas to make numbers pretty for displaying. */
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function progressionChartData(dailyData) {
    var newChartData = []
    for (var i=dailyData.length - 1; i >= 0 ; i--) {
        var newElement = [];
        newElement[0] = dailyData[i]['date'] 
        newElement[1] = dailyData[i]['cases']
        newChartData.push(newElement);
    }
    return newChartData
}

export function compareCases(a, b) {
    if (a['cases'] > b['cases']) return -1;
    if (b['cases'] > a['cases']) return 1;

    return 0;
}
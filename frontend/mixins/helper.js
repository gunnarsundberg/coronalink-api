/* Collection of helper functions */

/* Adds commas to make numbers pretty for displaying. */
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function progressionChartData(dailyData) {
    var newChartData = []
    for (var i=dailyData.length - 1; i >= 0 ; i--) {
        var newElement = [];
        console.log(i)
        newElement[0] = dailyData[i]['date'] 
        newElement[1] = dailyData[i]['cases']
        newChartData.push(newElement);
    }
    return newChartData
}

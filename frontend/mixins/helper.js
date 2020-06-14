/* Collection of helper functions */

/* Adds commas to make numbers pretty for displaying. */
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function progressionChartData(dailyData) {
    var newChartData = []
    for (var i=dailyData.length - 1; i >= 0 ; i--) {
        var newElement = [];    
        if (dailyData[i]['cases']) {
            newElement[0] = dailyData[i]['date']
            newElement[1] = dailyData[i]['cases']
        }
        else {
            var date = dailyData[i]['date'].toString()
            newElement[0] = date.replace(/(\d{4})(\d{2})(\d{2})/, "$1-$2-$3")
            newElement[1] = dailyData[i]['positive']
        }
        newChartData.push(newElement);
    }
    return newChartData
}

export function compareCases(a, b) {
    if (a['cases'] > b['cases']) return -1;
    if (b['cases'] > a['cases']) return 1;

    return 0;
}

export function percentChange(initialData, newData) {
    return ((((newData - initialData)/initialData) * 100).toFixed(1))
}

export function deathIncrease(newDeaths, initialDeaths) {
    return newDeaths - initialDeaths
}

export function caseIncrease(newCases, initialCases) {
    return newCases - initialCases
}
/* Collection of helper functions */

/* Adds commas to make numbers pretty for displaying. */
export function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function caseChartData(dailyData) {
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
            newElement[1] = dailyData[i]['positiveIncrease']
        }
        newChartData.push(newElement);
    }
    return newChartData
}

export function testingChartData(dailyData) {
    var newChartData = []
    for (var i=dailyData.length - 1; i >= 0 ; i--) {
        var newElement = [];    
        newElement[0] = dailyData[i]['date']
        newElement[1] = dailyData[i]['total_tested']
        newChartData.push(newElement);
    }
    return newChartData
}

export function compareCases(a, b) {
    if (a['cases'] > b['cases']) return -1;
    if (b['cases'] > a['cases']) return 1;

    return 0;
}

export function compareTests(a, b) {
    if (a['total_tested'] > b['total_tested']) return -1;
    if (b['total_tested'] > a['total_tested']) return 1;

    return 0;
}

export function compareWeighted(a, b) {
    if (a['weighted_tests'] > b['weighted_tests']) return -1;
    if (b['weighted_tests'] > a['weighted_tests']) return 1;

    return 0;
}

export function getObjectRank(array, key, value) {
    for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
            return i+1;
        }
    }
    return null;
}

export function findObject(array, key, value) {
    for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
            return array[i];
        }
    }
    return null;
}

export function ordinalSuffixOf(i) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

export function percentChange(initialData, newData) {
    return ((((newData - initialData)/initialData) * 100).toFixed(1))
}

export function displacement(newData, initialData) {
    return newData - initialData
}
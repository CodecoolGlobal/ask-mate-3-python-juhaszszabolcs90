// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //

    items.sort((a, b) => {
        let numberFields = ['VoteCount', 'ViewNumber']
        let valueA = numberFields.includes(sortField) ? parseInt(a[sortField]) : a[sortField]
        let valueB = numberFields.includes(sortField) ? parseInt(b[sortField]) : b[sortField]
        if (valueA < valueB ) {
            return sortDirection === 'asc' ? -1 : 1;
        }
        if (valueA  > valueB ) {
            return sortDirection === 'asc' ? 1 : -1;
        }
        return 0;
    })
    return items
}
// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}
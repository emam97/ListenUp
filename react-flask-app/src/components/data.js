// Prepare data only handles DonutChart right now
export function prepareData(data) {
    // Assume data is single response right now

    // If data is for entities, do this
    if (!data.type) {
        return data.map((entity , index) =>
            {
                const container = {}
                container.quantity = entity.count
                container.percentage = 1/data.count
                container.name = entity.text
                container.id = index
                return container
            })
    } else {
        // else if data is for keywords do this
        return data.map(keyword =>
            {
                const o = Object.keys(keyword.emotion).map((emotion, _i) => 
                {
                    const container = {}
                    container.name = emotion
                    container.group = keyword.text
                    container.value = keyword.emotion[emotion]
                    return container
                })
                return o
            }
        )
    }
}
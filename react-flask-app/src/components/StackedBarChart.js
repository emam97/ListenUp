import React from 'react';
import {StackedBar, ResponsiveContainer} from 'britecharts-react';
import PropTypes from 'prop-types';

function prepareData(data) {
    const list = []
    data.forEach(keyword =>
        {
            Object.keys(keyword.emotion).forEach((emotion, _i) => 
            {
                const container = {}
                container.name = keyword.text
                container.stack = emotion
                container.value = keyword.emotion[emotion]
                list.push(container)
            })
        }
    )
    return list
}

class StackedBarChart extends React.Component {
    render() {
        return <StackedBar
            data={prepareData(this.props.data)}
        />
    }
}

StackedBarChart.propTypes = {
    data: PropTypes.array
};

export default GroupedBarChart;
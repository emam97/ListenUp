import React from 'react';
import {Donut} from 'britecharts-react';
import PropTypes from 'prop-types';

function prepareData(data) {
    return data.map((entity , index) =>
            {
                const container = {}
                container.quantity = entity.count
                container.percentage = 1/data.length
                container.name = entity.text
                container.id = index
                return container
            })
}

class DonutChart extends React.Component {
    render() {
        return <Donut
            data={prepareData(this.props.data)}
        />
    }
}

DonutChart.propTypes = {
    data: PropTypes.array
};

export default DonutChart;
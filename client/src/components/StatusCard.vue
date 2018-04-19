<template>
  <div id="mountNode"></div>
</template>

<script>
  import G2 from '@antv/g2';
  import DataSet from '@antv/data-set';

  export default {
    props: ['data'],
    name: "status-card",
    methods: {
      randerChart() {
        const {DataView} = DataSet;

        const data = this.data;
        const dv = new DataView();
        dv.source(data).transform({
          type: 'percent',
          field: 'value',
          dimension: '_id',
          as: 'percent'
        });
        const chart = new G2.Chart({
          container: 'mountNode',
          forceFit: true,
          height: '200',
        });
        chart.source(dv, {
          percent: {
            formatter: val => {
              val = (val * 100) + '%';
              return val;
            }
          }
        });
        chart.coord('theta', {
          radius: 0.75
        });
        chart.tooltip({
          showTitle: false,
          itemTpl: '<li><span style="background-color:{color};" class="g2-tooltip-marker"></span>{_id}: {value}</li>'
        });
        chart.intervalStack()
          .position('percent')
          .color('_id')
          .label('percent', {
            formatter: (val, item) => {
              console.log(item)
              return item.value + ': ' + val;
            }
          })
          .tooltip('_id*percent', (item, percent) => {
            percent = percent * 100 + '%';
            return {
              name: item,
              value: percent
            };
          })
          .style({
            lineWidth: 1,
            stroke: '#fff'
          });
        chart.render();
      }
    }, mounted() {
      this.randerChart();
      console.log(this.data)
      this.$nextTick(function () {

      });
    },
  }
</script>

<style>
  @import "../style/github01.css";
  @import "../style/github02.css";
</style>

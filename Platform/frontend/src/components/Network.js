import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import Graph from "react-graph-vis";
import Grid from '@material-ui/core/Grid';
import 'fontsource-roboto';
import { makeStyles,createMuiTheme,ThemeProvider } from '@material-ui/core/styles';
import MaterialTable from 'material-table';
import { Line, Bar } from "react-chartjs-2";
import pattern from 'patternomaly';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';


// Design configurations are set
const useStyles = makeStyles((theme) => ({
  navbar : {
    flexGrow: 1
  },formControl: {
    margin: theme.spacing(1),
    minWidth: 140,
  },
  gridBorder: {
    border: "1px solid #1092dd",
    borderRadius: 16,
    padding: '2'
    
  },
  gekkig: {
    alignItems: 'left'
  },
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    '& > *': {
      margin: theme.spacing(1),
    }
    },
  table: {
    minWidth : 300,
  }
}));



function Network() {

  const classes = useStyles();
  
  const theme = createMuiTheme({
    palette: {
      primary: {
        main: '#1092dd',
      },
      secondary: {
        main: '#1092dd',
      }
    },
  });

  // UseStates are defined. 
  const [networkData, setNetworkData] = useState({});
  const [networkDataSlice, setNetworkDataSlice] = useState({});
  const [networkTableData, setNetworkTableData] = useState();
  const [networkTableColumns,setNetworkTableColumns] = useState();
  const [vendorInfo, setVendorInfo] = useState({});
  const [vendorInfoSlice, setVendorInfoSlice] = useState({});
  const [timestamps, setTimestamps] = useState();
  const [timestamp, setTimestamp] = useState()
  const [collectionType, setCollectionType] = useState('')
  const [graphData, setGraphData] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [openNetwork, setOpenNetwork] = useState(false);
  const [date, setDate] = useState()

  // UseEffect to load all the data once the page renders
  useEffect( async() => {
    const results = await axios.get('http://0.0.0.0:4000/network');
    var dataObject = {};
    for (const [key, value] of Object.entries(results.data[0])) {
      const json_value = JSON.parse(value)
      dataObject[key] = json_value
    }
    var dataObjectVendors = {};
    for (const [key, value] of Object.entries(results.data[1])) {
      const json_value = JSON.parse(value)
      dataObjectVendors[key] = json_value
    }
    setNetworkData(dataObject);
    setVendorInfo(dataObjectVendors);
    setTimestamps(Object.keys(results.data[2]));
    setTimestamp(Object.keys(results.data[2])[0])
    setDate(Object.keys(results.data[2])[0])
    
    setCollectionType('Text analysis')
    setNetworkDataSlice(dataObject[Object.keys(results.data[2])[0]]);
    setVendorInfoSlice(dataObjectVendors[Object.keys(results.data[2])[0]]);
    setNetworkTableData(Object.values(results.data[2])[0])
    setNetworkTableColumns(results.data[3])
    setGraphData(results.data[4])

    setLoaded(true);

  }, [])  

  // Table columns
  const determineColumns = () => {
    var columns = []
    for (const key of networkTableColumns){
      columns.push({title:key, field:key})
    }
    console.log(columns)
    return columns
  }

  


  // The settings for the network graph are set. 
    const options = {
        autoResize: true,
        width : '1100px',
        height : '580px',
        nodes: {
          shape: "dot",
          size: 16,
          color: {
            border:"#1092dd",
            background:"#1092dd",
            highlight: "#1092dd"
          },
        },
        layout: {
          improvedLayout: true
        },
        interaction: {
          dragNodes:true
        },
        physics:{
          enabled: true,
          barnesHut: {
            gravitationalConstant: -4000,
            centralGravity: 0.01,
            springLength: 150,
            springConstant: 0.04,
            damping: 0.09,
            avoidOverlap: 0
          }
        }

        
      };

      // Required for the network graph
    const events = {
      select: function(event) {
        var { nodes, edges } = event;
      }
    };

 

  
  // Handle changes in the graph when a different week is selected
      const handleChangeTimestamp = (event) => {
        setTimestamp(event.target.value);
        setNetworkDataSlice(networkData[timestamp])
        setVendorInfoSlice(vendorInfo[timestamp])
        setDate(event.target.value)
      };

      const handleChangeCollectionType = (event) => {
        setCollectionType(event.target.value);
      }


      // This function alters the input data in such a way that it can be used for the area chart
      const graphFunction = (dataToUse) => {
        var colours = ['#4053d3', '#ddb310']
        var patternChoice = ['dash', 'dot']
        var colourCounter = 0
        var allData = []
        for (const [category, weeks] of Object.entries(dataToUse)){
          var dataForWeeks = []
          for (const [week, amount] of Object.entries(weeks)){
            dataForWeeks.push(amount)
          }
          allData.push(
            {
              label: category,
              data: dataForWeeks,
              fill: true,
              backgroundColor: pattern.draw(patternChoice[colourCounter], colours[colourCounter]),
              borderColor: colours[colourCounter]
            })
            colourCounter += 1
        }

        console.log({
          labels : timestamps,
          datasets: allData
        })
    
        return ({
          labels : timestamps,
          datasets: allData
        })

      }

      const handleClickOpenNetwork = () => {
        setOpenNetwork(true);
      };
    
      const handleCloseNetwork = (event) => {
        setOpenNetwork(false);
      };



    if (loaded){

      const columns = determineColumns()
      const data = networkTableData

      return (
        <div className={classes.gekkig}>
          
          
          <Grid container direction="row" justify="flex-start" alignItems="center">
          
                  <Grid item xs={8} align="center">
                  <FormControl className={classes.formControl}>
                          <InputLabel id="demo-simple-select-label" >Collection date</InputLabel>
                          <Select
                          labelId="demo-simple-select-label"
                          id="demo-simple-select"
                          value={timestamp}
                          
                          onChange={handleChangeTimestamp}
                          >

                          {timestamps.map((x) => (
                          <MenuItem value={x}>{x}</MenuItem>
                              )

                          )}
                          </Select>
                          <FormHelperText>Select scraper date</FormHelperText>
                      </FormControl>
                      </Grid>
                      <Grid item xs={4}></Grid>
                      </Grid>
                      <br></br>
                      <Grid container direction="row" justify="flex-start" alignItems="center">
                      <Grid item xs={8}>
                        <Graph
                          graph={networkDataSlice}
                          options={options}
                          events={events}
                          getNetwork={network => {
                            //  if you want access to vis.js network api you can set the state in a parent component using this property
                          }}/>

                      </Grid>
               
          {/* AREA CHART SECTION */}
            <Grid item xs={4}>

                                  
                    <Line 
                    data={graphFunction(graphData)}
                      
                      
                  
                    options = {{
                      scales: {
                        yAxes: [{
                          stacked: true,
                          scaleLabel: {
                            display: true,
                            labelString: 'Number of vendors'
                          }
                        }],
                        xAxes: [{
                          scaleLabel: {
                            display: true,
                            labelString: 'Date of data collection'
                          }
                        }],
                      }     
                    }}
                    />
                    
             
                
               
              </Grid>
              </Grid>

              {/* TABLE SECTION */}
              <Grid container justify="center">
              <Grid item xs={10} >
              <div class="table-container">
              <MaterialTable title="Targeted markets based on textual analysis of vendor information section"
                  data = {data}
                  columns={columns}
                  options={{
                    exportButton:true,
                    pageSize:100,
                    headerStyle: {
                      fontWeight: 'bold',
                      color: '#000000'
                  }}} 
                  
         
       />
                </div>
              </Grid>
              </Grid>
              
              
              
            
              
  
        </div>
  
      );
    } else {
      return (
        <div></div>
      )
      }
  };

  export default Network;


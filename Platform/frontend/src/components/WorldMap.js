import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import { WorldMap } from "react-svg-worldmap"
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Line } from "react-chartjs-2";
import InputLabel from '@material-ui/core/InputLabel';
import ListItemText from '@material-ui/core/ListItemText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';
import Input from '@material-ui/core/Input';
import Slider from '@material-ui/core/Slider';
import Button from '@material-ui/core/Button';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import CheckIcon from '@material-ui/icons/Check';
import DialogActions from '@material-ui/core/DialogActions';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Dialog from '@material-ui/core/Dialog';


// Set design configurations
const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
    maxWidth: 300,
  },
  gridBorder: {
    border: "1px solid #1092dd",
    borderRadius: 16,
    padding: '2'
    
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: 2,
  },
  noLabel: {
    marginTop: theme.spacing(3),
  },
    navbar : {
      flexGrow: 1
    },
    gekkig: {
      alignItems: 'left'
    },
    slider: {
      width: 300,
    },
    root: {
      justify: 'center',
      padding: "40px",
      direction: 'column',
      alignItems: 'center',
      '& > *': {
        margin: theme.spacing(1),
      }
      },
  }));
  


function Worldmap() {

    const classes = useStyles();

    // Set useStates
    const [openInfo, setOpenInfo] = useState(false);
    const [timestampSalesButtons, setTimestampSalesButtons] = useState({});
    const [mapData, setMapData] = useState({});
    const [mapDataSlice, setMapDataSlice] = useState({});
    const [graphLabels, setGraphLabels] = useState({});
    const [graphData, setGraphData] = useState({});
    const [graphDataSelector, setGraphDataSelector] = useState({});
    const [selectedGraphData, setSelectedGraphData] = useState([]);
    const [loaded, setLoaded] = useState(false);


    // Load data
    useEffect( async() => {
        const results_reviews = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/reviews");
        for (const [key, value] of Object.entries(results_reviews.data[1])){
          setTimestampSalesButtons(Object.keys(value))
          console.log(Object.keys(value))
          break
        }
        
        setMapData(results_reviews.data[2])
        setGraphLabels(Array.from(Object.keys(results_reviews.data[3]['United States'])))
  
        setSelectedGraphData(Object.keys(results_reviews.data[3]))
        var graphDataNames = []
        for (const [key,value] of Object.entries(results_reviews.data[3])){
          if (!(key.includes('max') || key.includes('min'))){
            graphDataNames.push(key)
          }
        }
        setGraphDataSelector(graphDataNames)
        console.log(graphDataNames)
        setGraphData(results_reviews.data[3])

        // Set initial slice for worldmap
        setMapDataSlice(results_reviews.data[2]["2021- week 1"])
        setLoaded(true);
        
    
      }, [])  

       
 

  // This function transforms the input data in such a way that it can be shown by the linegraph 
  const lineData = () => {
    var differentColours = ['rgb(47,75,124)','rgb(102,81,145)',"rgb(0,63,92)", 'rgb(160,81,149)', 'rgb(212,80,135)','rgb(249,93,106)', 'rgb(255,124,67)', 'rgb(255,166,0)' ]
    var differentColoursMaxMin = ["rgb(0,63,92,0.5)", 'rgb(47,75,124,0.5)','rgb(102,81,145,0.5)', 'rgb(160,81,149,0.5)', 'rgb(212,80,135,0.5)','rgb(249,93,106,0.5)', 'rgb(255,124,67,0.5)', 'rgb(255,166,0,0.5)' ]
    //var differentColours = ["#005073","#107dac","#189ad3","#1ebbd7","#71c7ec"]
    var allData = []
    var i = 0
    var dataToIterate = selectedGraphData
    var dictToIterate = {};
    Object.entries(graphData).forEach(([key,value]) => {
      if (dataToIterate.includes(key)){
        dictToIterate[key] = value
      }
    })
    
    Object.entries(dictToIterate).forEach(([key,value]) => {
      if (!(key.includes('max') || key.includes('min'))){
        allData.push({
          label: key,
          data: Object.values(value),
          fill: false,
          borderColor: differentColours[i]
        })
        Object.entries(dictToIterate).forEach(([MaxMinKey,MaxMinvalue]) => {
          if (MaxMinKey.includes(key) && MaxMinKey != key){
            allData.push({
              label: MaxMinKey,
              data: Object.values(MaxMinvalue),
              fill: false,
              borderDash: [10,2],
              backgroundColor: differentColours[i]
            })
          }
        })
      }
      
      // Done to loop through the list of colours; if the end is reached, continue at the start again
      if (i !== 7){
        i++;
      } else{
        i = 0;
      }
      
      });
      return({
        labels: graphLabels,
        datasets: allData
      })


    
  }
  
  // Functions for the select box
  const handleChange = (event) => {
    var dataToLoop = event.target.value
    console.log(dataToLoop)
    var selectedCountry = []
    for (var element of dataToLoop){
      selectedCountry.push(element)
      selectedCountry.push(element.concat("_max"))
      selectedCountry.push(element.concat("_min"))
    }
    console.log(selectedCountry)
  

    
    setSelectedGraphData(selectedCountry);
    lineData(selectedGraphData);
    console.log(selectedGraphData)
    
  };

  // Settings for the select country box
  const ITEM_HEIGHT = 200;
  const ITEM_PADDING_TOP = 8;
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        width: 250,
      },
    },
  };

  function valuetext(value) {
    return `${value}°C`;
  }

  const allCountryLabels = graphDataSelector

  const handleCloseInfo = (event) => {
    setOpenInfo(false);
  };
  const handleOpenInfo = () => {
    setOpenInfo(true);
  };





    if (loaded){
        
        // Function used for the slider length
        const ultimateTransform = () => {
          var finalData = [];
          var i = 0;
          timestampSalesButtons.forEach(function (item){
            finalData.push({
              value:i,
              label:item
            })
            i += 100/(timestampSalesButtons.length-1)
          })
      
          return (finalData)
        }
      
        const sliderData = ultimateTransform();
        // Function for the buttonvalue for the slider
        function valueLabelFormat(value) {
          var index = sliderData.findIndex((mark) => mark.value === value);
          var date = sliderData[index]["label"];
          setMapDataSlice(mapData[date]);
          return date.substr(5,6)
        }
      
        
        return (
          
            <div className="gekkigheid" >
              <br></br>
                <Grid container direction={'row'} spacing={2}>
                <Grid item xs={6}  >
                  <div className={classes.root}>
                    {/* SLIDER SECTION */} 
                    <Slider
                      defaultValue={sliderData[0]['value']}
                      valueLabelFormat={valueLabelFormat}
                      getAriaValueText={valuetext}
                      aria-labelledby="discrete-slider-restrict"
                      step={null}
                      
                      marks={sliderData}
                      valueLabelDisplay="on"
                    />

                  </div>
                
                </Grid>
                <Grid  item xs={6}>
                  {/* COUNTRY SELECTOR SECTION */} 
                  <Grid container direction="row">
                    <Grid item xs={4}>
                      <FormControl className={classes.formControl}>
                        <InputLabel id="demo-mutiple-checkbox-label">Countries</InputLabel>
                        <Select
                          labelId="demo-mutiple-checkbox-label"
                          id="demo-mutiple-checkbox"
                          multiple
                          value={selectedGraphData}
                          onChange={handleChange}
                          input={<Input />}
                          renderValue={(selected) => selected.join(', ')}
                          MenuProps={MenuProps}
                        >
                          {allCountryLabels.map((name) => (
                            <MenuItem key={name} value={name}>
                              <Checkbox checked={selectedGraphData.indexOf(name) > -1} />
                              <ListItemText primary={name} />
                            </MenuItem>
                          ))}
                        </Select>
                        <br></br>
                        
                       
                      </FormControl>
                      </Grid>
                      &nbsp;&nbsp;
                      <Grid item xs={2}>
                        <br></br>
                    <Button variant="contained" size="small" color="primary" onClick={() => {setSelectedGraphData([])}}>
                      Deselect all</Button>
                    </Grid>
                    <Grid item xs={1}>
                    <br></br>
                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleOpenInfo} />
                  {/* INFORMATION SECTION */} 
                  <Dialog
                        open={openInfo}
                        onClose={handleCloseInfo}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Country sales
                    </DialogTitle>
                    <DialogContent>
                    <DialogContentText>
                    This tab shows how the sales per shipping country evolve over time. As the actual sales are not known
                    on the dark market, the amount of reviews serve as a proxy (good indicator). The calculation of the sales
                    is explained in the 'sales per market' tab.
                    </DialogContentText>
                    <DialogContentText>
                      The slider on the left hand page allows you to track the of sales over time. The color indicates how much
                      a country is shipping in <b>relation</b> to other countries. The graph on the right reports the <b>absolute </b> 
                       sales per country.
                    </DialogContentText>
                    <DialogContentText>
                     The graph on the right includes the category "unknown". If the vendor reports no information regarding
                     the origin of destination of shipments, he is included under this category.
                    </DialogContentText>
                    <DialogContentText>
                      The graph reports an interval per country, since some products are reported to be possibly shipped from a 
                      multitude of countries. Therefore, the min and max line per country give an indication of the uncertainty
                      of sales.
                    </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfo} color="primary">
                        Close
                      </Button>
                    </DialogActions>
                    
                    </Dialog>  
                      </Grid>                    
                    </Grid>
                    </Grid>
                    </Grid>


                  {/* WORLDMAP SECTION */} 
                    <Grid container direction={'row'} spacing={2}>
                        <Grid item className={classes.mapWorld} xs={6}>
                          
                          <WorldMap color="#FF0000"  value-suffix="people" size='responsive' data={mapDataSlice} />
                          
                            
                            </Grid>
           
                  {/* LINEGRAPH SECTION */} 
                    <Grid item xs={5} align="center">
                    <Line data = {lineData(selectedGraphData)} 
                    options = {{responsive: true,
                      legend: {
                        display: false
                      },
                          scales: {yAxes: [{
                            scaleLabel: {
                              display: true,
                              labelString: 'Estimated revenue'
                            },
                            ticks: {
                              beginAtZero: true,
                              callback: function(value, index, values) {
                                if(parseInt(value) >= 1000){
                                  return '€' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                                } else {
                                  return '€' + value;
                                }
                              }
                            }
                          }],
                            xAxes: [{
                              scaleLabel: {
                                display: true,
                                labelString: 'Date in weeks'
                              }
                              }]}}} />
                      </Grid>
                    </Grid>
                
                
              
            </div>
          )
    } else {
        return (
            <Grid
              container
              spacing={0}
              direction="column"
              alignItems="center"
              justify="center"
              style={{ minHeight: '100vh' }}
            >
      
              <Grid item xs={3}>
                <CircularProgress />
              </Grid>   
      
      </Grid>  
          );
          
    }

  
}

export default Worldmap;




import Grid from '@material-ui/core/Grid';
import { ResponsiveTreeMap } from '@nivo/treemap'
import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Line, Bar } from "react-chartjs-2";
import { Bubble } from 'react-chartjs-2';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Worldmap from './WorldMap'
import MyTheme from './MyTheme'
import { useHistory,Link  } from 'react-router-dom';
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';
import Video from '../sales.mp4'
import VideoPlayer from 'react-video-js-player'
import Dialog from '@material-ui/core/Dialog';
import MessageIcon from '@material-ui/icons/Message';
import commentBox from 'commentbox.io';
import Comments from "./Comments"
import DialogActions from '@material-ui/core/DialogActions';
import Tour from 'reactour'
import Typography from '@material-ui/core/Typography';
import { useLocation } from 'react-router-dom';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Box from '@material-ui/core/Box';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import CheckIcon from '@material-ui/icons/Check';
import WarningIcon from '@material-ui/icons/Warning';




// Set design configurations
const useStyles = makeStyles((theme) => ({
  gridBorder: {
    border: "1px solid #1092dd",
    borderRadius: 16,
    padding: '2'
    
  },
  navbar : {
    flexGrow: 1
  },
  gekkig: {
    alignItems: 'left'
  },
  root: {

      direction: 'column'
    },
  table: {
    minWidth : 300,
  },
  buttons: {
    display: 'flex',
    justifyContent: "center",
    alignItems:"center"
  },
  agarthaColour:{
    colour: "#1092dd"
  }
}));





export default function Salespage() {

    var classes = useStyles();
    const location = useLocation();
    const history = useHistory();
  

  // This function is used to make sure that the tour functionality can be used
  // Once the page loads, it detects whether anything is present in the location.state
  // If that is the case, the tour is set to true
  // It will be called further on in the script
    function runIt(){
          if (location.state !== undefined){
            console.log(location.state[0])
              if ( location.state[0] === true){
                setIsTourOpen(true)
                  location.state = '';
                  return(null)
               }
              
          }
              
          }
        // These are all the steps of the tour. All of them have to be defined here to make sure that the dots corresponding
        // to the amount of steps left are correct
          const steps = [
           
            {
              content: 'This is my first Step',
              action: () => history.push({pathname: '/overview',state: [true]})
              
            },
            {
              content: <Typography variant="subtitle1">
                Welcome to the Anita dashboard! This tour will tell you all you need to know to get going.
              </Typography>
            },
            {
              content: <div><Typography variant="subtitle1">
              This dashboard aims to make you more knowledgable regarding drug trafficking that takes place on the dark web.
              It is focussed on people that sell drugs, so called vendors. 
            </Typography>
            <Typography variant="subtitle1">
             It contains data, information and intelligence 
          </Typography>
          </div>
            },
            {
              selector:'.data',
              content: <Typography variant="subtitle1">
                The 'raw data' tab allows you to study all the data that has been used throughout the dashboard. Data can be considered
                as the unaltered observations made on the dark web. After this data was collected, personal data 
                was deleted and the aliases of users were pseudonimized.
              </Typography>
            },
            {
              content: 'This is my first Step',
              action: () => history.push({pathname: '/producttable',state: [true]})
              
            },
            {
              selector:'.producttable',
              content: <Typography variant="subtitle1">
                The tables allow you to sort and search for specific words.
              </Typography>
            },
            {
              content: <Typography variant="subtitle1">
                Information can be perceived as a usefull combination of data that increases its value.
                The information sections have been divided by means of the 5 W's central to an investigation.
              </Typography>
            },
            {
              selector:'.operational',
              content: <Typography variant="subtitle1">
                Operational information refers to the "Who" question, therefore allowing you to identify interesting vendors.
              </Typography>
            },
            {
              action: () => history.push({pathname: '/operational',state: [true]})
              
            },
            {
                selector:'.select',
                content: <Typography variant="subtitle1">
                  These selectors allow you to filter out vendors of your interest
                </Typography>
              },
              {
                selector:'.go',
                content: <Typography variant="subtitle1">
                  After clicking go, you will be presented with the vendors, sorted by estimated revenue
                </Typography>
              },
              {
                selector:'.tactical',
                content: <Typography variant="subtitle1">
                  The tactical information tab will tell you more about the "where", "how" and "what" questions.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/treemap',state: [true]})
                
              },
              {
                selector:'.treemapbuttons',
                content: <Typography variant="subtitle1">
                  The "where" section allows you to study the sales development on market, country and vendor level
                </Typography>
              },
              {
                content: <div>
                <Box fontWeight="fontWeightBold" align="center">Be aware!</Box> 
                <br></br>
                <Typography variant="subtitle1">
                  The presented sales are an estimation based on the reviews on the marketplace. Since these differ in 
                  quality and precision per marketplace, it is adviced to read the information section, which can be 
                  opened by clicking a similar icon to the one below. These can be found throughout the dashboard and
                  provide you with extra information.
                </Typography>
                <InfoOutlinedIcon align="center" style={{color:'#1092dd', fontSize:30}} />
                </div>
              },
              {
                action: () => history.push({pathname: '/mo',state: [true]})
                
              },
              {
                content: <Typography variant="subtitle1">
                  The "how" section provides you with information related to the business plan of vendors. 
                </Typography>
              },
              {
                selector:'.mobuttons',
                content: <Typography variant="subtitle1">
                  By clicking on a tab, a specific part of the business plan of vendors gets highlighted. 
                  Comparisons between countries and marketplaces can be made.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/product',state: [true]})
                
              },
              {
                content: <Typography variant="subtitle1">
                  The "what" page allows you to study the types of products that are shipped from specific countries
                  and marketplaces. By clicking on the drug categories in the table below you can see what drugs
                  belong to a certain category.
                </Typography>
              },
              {
                content: <Typography variant="subtitle1">
                 Lastly, the dashboard also provides you with intelligence. By combining various information sources,
                 intelligence can enhance decision-making capabilities. This process often involves effort from you,
                  the analysts. To aid you with this process, this dashboard allows you to store your relevant
                 insights and share these with others, learning from each other. 
                </Typography>
              },
              {
                selector:'.commentButton',
                content: <Typography variant="subtitle1">
                  When clicking on this icon, a comment section appears. Once you have logged in, you can comment, reply
                  and like other comments. Together we know more!
                </Typography>
              },
              {
                selector:'.mindmap',
                content: <Typography variant="subtitle1">
                 Additionally, clicking over here allows you to create a mindmap that only you can see, keeping track of
                 the insights you have obtained.
                </Typography>
              },
              {
                selector:'.mindmap',
                content: <Typography variant="subtitle1">
                 That was the tour! You will now be redirected to the overview page, giving you an initial impression
                 of what you can expect.
                </Typography>
              },
              {
                action: () => history.push({pathname: '/overview'})
                
              },
          
          ];

    // Set all useStates
    const [open, setOpen] = useState(false);
    // Set useStates for the information sections
    const [openInfoCannazon, setOpenInfoCannazon] = useState(false);
    const [openInfoAgartha, setOpenInfoAgartha] = useState(false);
    const [openInfoTreemap, setOpenInfoTreemap] = useState(false);
    const [openInfoScatterplot, setOpenInfoScatterplot] = useState(false);
    const [openComments, setOpenComments] = useState(false);
    const [treemapData, setTreemapData] = useState({});
    const [colors, setColors] = useState({});
    // useState for the linegraph
    const [linegraph, setLinegraph] = useState({});
    const [linegraphSlice, setLinegraphSlice] = useState({});
    const [selectedName, setSelectedName] = useState({});
    const [scatterplotData, setScatterplotData] = useState({});
    const [dataToRender, setDataToRender] = useState();
    const [dataMarket, setDataMarket] = useState({});
    // These useStates are defined to open/close a functionality based on the tab that is clicked by the user
    const [showResultsTreemap, setShowResultsTreemap] = useState(false)
    const [showResultsMarket, setShowResultsMarket] = useState(false)
    const [showResultsWorldmap, setShowResultsWorldmap] = useState(false);
    const [vendorOperationalTab,setVendorOperationalTab] = useState('');
    const [showResultsScatterplot, setShowResultsScatterplot] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [isTourOpen, setIsTourOpen] = useState(false);

  
  // Set useStates to highlight button if it is clicked
    const [button1, setButton1] = useState(false);
    const [button2, setButton2] = useState(false);
    const [button3, setButton3] = useState(false);
    const [button4, setButton4] = useState(false);



  // These functions are used to open/close information sections + the comment section 
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClickOpenComments = () => {
      setOpenComments(true);
    };
  const handleClose = (event) => {
      setOpen(false);
    };
    const handleCloseComments = (event) => {
      setOpenComments(false);
    };
  const handleCloseInfoCannazon = (event) => {
    setOpenInfoCannazon(false);
  };
  const handleOpenInfoCannazon = () => {
    setOpenInfoCannazon(true);
  };
  const handleCloseInfoAgartha = (event) => {
    setOpenInfoAgartha(false);
  };
  const handleOpenInfoAgartha = () => {
    setOpenInfoAgartha(true);
  };
  const handleCloseInfoTreemap = (event) => {
    setOpenInfoTreemap(false);
  };
  const handleOpenInfoTreemap = () => {
    setOpenInfoTreemap(true);
  };
  const handleCloseInfoScatterplot = (event) => {
    setOpenInfoScatterplot(false);
  };
  const handleOpenInfoScatterplot = () => {
    setOpenInfoScatterplot(true);
  };


  // Load the data
    useEffect( async() => {
     
        const results = await axios.get('http://0.0.0.0:4000/reviews');
        setTreemapData(results.data[5])
        var all_vendors_colours = {}
        for (const [market, colours] of Object.entries(results.data[7])){
          for (const [vendor, colour] of Object.entries(colours)){
            all_vendors_colours[vendor] = colour
          }
        }
        setColors(all_vendors_colours)
        
        setLinegraph(results.data[8])
        // Set data for the linegraph at the treemap
        for (const [key, value] of Object.entries(results.data[8]['agartha'])){
          setLinegraphSlice(value)
          setSelectedName(key)
          break
        }
        setScatterplotData(results.data[9])
        setDataMarket(results.data[1])
        setLoaded(true)
    }, []) 

  // Load commentbox functionality  
  useEffect( async() => {
    var comment = commentBox('5753003650842624-proj')
  })



    // This function transform the input data in such a way that it can be used for the line graph in the 'sales per market' 
    const marketFunction = (dataToUse) => {
      var allData = []
      var colours = ['rgb(24,154,211)', 'rgb(255,175,122)']
      var coloursFill = ['rgb(24,154,211,0.5)', 'rgb(255,175,122,0.5)']
      var colourCounter = 0
      for (const [market, sales] of Object.entries(dataToUse)){
        allData.push(
          {
            label: market,
            data: Object.values(sales),
            fill: false,
            backgroundColor: coloursFill[colourCounter],
            borderColor: colours[colourCounter]
          })
          colourCounter += 1
      }

      for (const [key, value] of Object.entries(dataToUse)){
        var timestamp = Object.keys(value)
        break
      }

      return ({
        labels: timestamp,
        datasets:allData
      })
    }

    // Function used for the scatterplot
    const scatterplotFunction = (dataToUse) => {
      var allData = []
      var colours = ['rgb(24,154,211)', 'rgb(255,175,122)']
      var coloursFill = ['rgb(24,154,211,0.5)', 'rgb(255,175,122,0.5)']
      var colourCounter = 0
      for (const [market, sales] of Object.entries(dataToUse)){
        allData.push(
          {
            label: market,
            data: Object.values(sales),
            fill: true,
            backgroundColor: coloursFill[colourCounter],
            borderColor: colours[colourCounter]
          })
          colourCounter += 1
      }

      for (const [key, value] of Object.entries(dataToUse)){
        var timestamp = Object.keys(value)
        break
      }

      return ({
        labels: timestamp,
        datasets:allData
      })
    }

   



    // This function makes sure the tab that is selected gets highlighted
    const buttonChange = (number) => {
      if (number === 1){
        setButton1(true)
        setButton2(false)
        setButton3(false)
        setButton4(false)
      }
      if (number === 2){
        setButton1(false)
        setButton2(true)
        setButton3(false)
        setButton4(false)
      }
      if (number === 3){
        setButton1(false)
        setButton2(false)
        setButton3(true)
        setButton4(false)
      } if (number === 4){
        setButton1(false)
        setButton2(false)
        setButton3(false)
        setButton4(true)
      }}
      
    if (loaded){
      
      runIt()
        console.log(colors)
        const getColor = bar => colors[bar.id]
        console.log(linegraphSlice)

        function handleChange(event) {
          const name = event.data['name']
          for (const [market, vendors] of Object.entries(linegraph)){
            if (name in vendors){
              setLinegraphSlice(linegraph[market][name])
              setSelectedName(name)
              setVendorOperationalTab(name)
              console.log(name)

            }
          }
          
          
        }

    
     
        
        return(

            <div className="second" >
              <Grid className={classes.buttons} item xs={12}>
              <br></br>
              <br></br>
              <br></br>
              <br></br>
              <div ><font size="3">Choose what kind of sales trend you want to investigate</font></div>
              <Button>
              <OndemandVideoIcon style={{color:'#FF6700', fontSize:30}} onClick={handleClickOpen} ></OndemandVideoIcon>
        </Button>
        <Dialog
                        open={open}
                        onClose={handleClose}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"md"}
                    >
                       
                        <VideoPlayer src={Video} width="720" height="420"></VideoPlayer>
                        <DialogActions>
                      <Button onClick={handleClose} color="primary">
                        Close
                      </Button>
                      
                    </DialogActions>
                        
                    </Dialog>  
                    <Button>
                        <MessageIcon style={{color:'#FF6700', fontSize:30}} onClick={handleClickOpenComments} ></MessageIcon>
                   </Button>  

                   <Dialog
                        open={openComments}
                        onClose={handleCloseComments}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"md"}
                        fullWidth = {true}
                    > 
                      
                        <Comments />
                        
                    </Dialog>
                    <Tour
                    steps={steps}
                    isOpen={isTourOpen}
                    onRequestClose={() => setIsTourOpen(false)}
                    startAt={13}
                    rounded={10}
                     />
                    
            </Grid>

            {/* ALL THE BUTTONS ARE CREATED */} 
            <Grid container className="treemapbuttons"
                direction="row"
                justify="center"
                alignItems="center" spacing={2}>
            <Grid  item xs='auto'   >
              <Button  variant={button1 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(1); setShowResultsScatterplot(false); setShowResultsWorldmap(false); setShowResultsTreemap(false); setShowResultsMarket(true) }}>Sales per market</Button>
            </Grid>
            <Grid  item xs='auto'   >
              <Button  variant={button2 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(2);setShowResultsScatterplot(false); setShowResultsMarket(false); setShowResultsTreemap(false); setShowResultsWorldmap(true)}}>Sales per country</Button>
            </Grid>
            <Grid  item xs='auto'   >
              <Button variant={button3 ? "contained" : "outlined"} size="small" color="primary" onClick= {() => {buttonChange(3); setShowResultsScatterplot(false); setShowResultsWorldmap(false); setShowResultsMarket(false); setShowResultsTreemap(true) }} >Sales per vendor (treemap)</Button>
            </Grid>
            <Grid  item xs='auto'   >
              <Button variant={button4 ? "contained" : "outlined"} size="small" color="primary" onClick= {() => {buttonChange(4);   setShowResultsWorldmap(false); setShowResultsMarket(false); setShowResultsTreemap(false);setShowResultsScatterplot(true) }} >Sales per vendor (scatterplot)</Button>
            </Grid>
           
            </Grid>
            <br></br>
            

          {/* SALES PER MARKET SECTION */} 
          {showResultsMarket ?  
          <Grid container spacing={2}>
          <Grid item xs={9}>
          <Line 
            data={marketFunction(dataMarket)}
              
              
          
            options = {{
              scales: {
                yAxes: [{
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
                    labelString: 'Date'
                  }
                }],
              }     
            }}
            />
            </Grid>
            <Grid item  xs={3}>
              <Grid item xs={12}>
            <br></br>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  flexWrap: 'wrap',
              }}> <span STYLE="font-size:18.0pt;margin-right: 1.5em">Cannazon</span>
                  <CheckIcon style={{color:'#00b300', fontSize:40}}  />
                  &nbsp;&nbsp;
                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleOpenInfoCannazon} />
                  
              </div>  
              </Grid> 
              <Grid item xs={12}>
              <br></br>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  flexWrap: 'wrap',
              }}> <span STYLE="font-size:18.0pt;margin-right: 2.4em">Agartha</span>
                  <WarningIcon style={{color:'#ffa500', fontSize:40}} />
                  &nbsp;&nbsp;
                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleOpenInfoAgartha} />
                  
              </div>  
              </Grid> 
          
                  <Dialog
                        open={openInfoCannazon}
                        onClose={handleCloseInfoCannazon}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Cannazon
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                      The sales of the <b>Cannazon</b> market are estimated by means of analyzing the reviews. Reviews are commonly attached to the vendor
                      page itself, not the products. They mention the product that is bought and the amount that is spent by the buyer.
                      Therefore, adding all of these amounts together gives a lower bound for the sales of this market. It is a lower bound since most 
                      likely not every buyer leaves a review. 
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfoCannazon} color="primary">
                        Close
                      </Button>
                    </DialogActions>
      
                    </Dialog>  
                    <Dialog
                        open={openInfoAgartha}
                        onClose={handleCloseInfoAgartha}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Drug categories
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                      The <b>Agartha</b> market provides reviews attached to the vendorpage, not the product pages. They rarely provide information 
                      about the product that is bought. Additionally, this market also sells other goods, not related to drugs. Therefore, it is not 
                      known with certainty whether a review is related to a drugs-related
                      product. To get an approximation of the drug sales, an estimate about the drug/non-drug ratio is made. This is done by 
                      textually analysing all the reviews within a certain week that contain a product name
                      This ratio is thereafter used to estimate how many of the reviews without any text were drug related. None of the reviews
                      mentioned the price that was spent. As such, it has been assumed that a review is equal to the sale of one product.
                      To derive the sales in euro's, all the drug offerings of a vendor in the next week were analysed. For example, all the sales that
                      were made in week 1 were assigned to the products data that was found at the beginning of the next week. Since it remains largly
                      unknown what products were sold, it was presumed that every product was sold equally often. As such, the average price of all 
                      product could be taken, which was finally multiplied by the amount of reviews that the vendor received.
                      </DialogContentText>
                      <DialogContentText>
                      For example, vendor X has
                      10 reviews in week 1. The calculated drug/non-drug ratio for that week is 0.8. This means that 8 
                      of his reviews are assumed to be devoted to drugs. From the data that was collected in week 2, it is known that Vendor X has 4
                      different products with an average price of €150. Based on the available data, his estimated revenue for week 1 is 
                      8 * €150 = €1200.Admittedly, this estimation is worse than from Cannazon, but the best that can be done with the provided data of the 
                      marketplace.
                      </DialogContentText>
                  
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfoAgartha} color="primary">
                        Close
                      </Button>
                    </DialogActions>
      
                    </Dialog>  
            
            </Grid>
            
           
            </Grid>
            :<div></div>}
        
        
          {/* SALES PER COUNTRY SECTION */}    
           {showResultsWorldmap ? <Worldmap /> : <div></div>}


          {/* SALES PER VENDOR (TREEMAP) SECTION */} 
          {showResultsTreemap ? 
          <Grid container >
          <Grid item xs={8}>
        <div className="treemap" style={{height:650, width:1100}}>
            <ResponsiveTreeMap 
          data={treemapData}
          identity="name"
          onClick = {handleChange}
          colors= {getColor}
          value="loc"
          valueFormat=".02s"
          margin={{ top: 10, right: 10, bottom: 10, left: 10 }}
          labelSkipSize={12}
          labelTextColor='black'
          parentLabelTextColor={{ from: 'color', modifiers: [ [ 'darker', 2 ] ] }}
          borderColor='black'
      /></div>
      </Grid> 
     
      <Grid item xs={4}>
      <Grid container style={{ gap: 25 }} spacing={2}>
        <Grid item xs={5}> <br></br> 
        <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:40}} onClick={handleOpenInfoTreemap} />
                      <Dialog
                        open={openInfoTreemap}
                        onClose={handleCloseInfoTreemap}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Treemap
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                      The treemap on the left gives insights into both the size and the development of vendors.
                      The size of the boxes correspond to the estimated revenue of the vendors the since the 
                      start of 2021 untill the last date collection date. Intuitively, the bigger a box, the more sales the
                      vendor has made. The colours of the boxes correspond to development of sales since the beginning
                      of 2021. The calculation is done as follows. All the weeks of data collection are split up into
                      two parts. Next, the average weekly revenues are calculated for both partitions. 
                      By calculating the percentual difference, a colour can be attributed to each vendor. Red indicates
                      the vendor increased his sales, whereas blue indicates descending sales. 
                      </DialogContentText>
                      <DialogContentText>
                        By clicking on a box, the sales of a vendor are plotted in a graph. Below the graph is a button
                        that automatically redirects you to the information section of this vendor.
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfoTreemap} color="primary">
                        Close
                      </Button>
                    </DialogActions>
      
                    </Dialog>  
                         
                         <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkestRed}></Button>
                                  &nbsp; Average increase more than 50%
                                  </Grid>
                                  
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.Red}></Button>
                                  &nbsp; Average increase of 0% - 50% 
                                  </Grid>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.No}></Button>
                                  &nbsp; No increase
                                  </Grid>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.lightBlue}></Button>
                                  &nbsp; Average decrease of 0% - 50% 
                                  </Grid>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.Blue}></Button>
                                  &nbsp; Average decrease more than 50% 
                                  </Grid>
                                  </Grid>
      
                                  
        <Grid item xs={11} align="center">
            <Line 
            data={{
              labels: Object.keys(linegraphSlice),
              datasets: [
                {
                  label: selectedName,
                  data: Object.values(linegraphSlice),
                  fill: false,
                  backgroundColor: "#1092dd",
                  borderColor: "#1092dd"
                },
              ]
            }}
            options = {{
              
              scales: {
                yAxes: [{
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
                    labelString: 'Date'
                  }

            }]
              }     
            }}
            />
            <br></br>
            <Grid container  direction="row" justify="center"alignItems="center">
            <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                         
               {vendorOperationalTab ?
                <Button variant="contained" size="small" color="primary" >
                Investigate {vendorOperationalTab} on the operational dasbhoard </Button>
                :  <Button variant="contained" size="small" color="primary" >
                To operational dasbhoard </Button>}
                
                </Link>
            </Grid>
            </Grid>
        </Grid>
        </Grid>
</Grid>: <div></div>}

      {/* SALES PER VENDOR (SCATTERPLOT) SECTION */} 

            {showResultsScatterplot ? 
              <Grid container spacing={2}>
              <Grid item xs={8}>
                <Bubble type= 'bubble'
    
                        data= {{
                            datasets: scatterplotData
                        }}
                        
                        options ={{
                          legend: {
                             display: false
                          },
                          scales: {yAxes: [{
                            scaleLabel: {
                              display: true,
                              labelString: 'Average weekly percentual change',
                            }}],
                            xAxes: [{
                              scaleLabel: {
                                display: true,
                                labelString: 'Estimated revenue since 2021- week 1'
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
                            }],}}}
                      />
              </Grid>
              <Grid item xs={4}> <br></br> 
                   <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:40}} onClick={handleOpenInfoScatterplot} />
                      <Dialog
                        open={openInfoScatterplot}
                        onClose={handleCloseInfoScatterplot}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Scatterplot
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                      The scatterplot on the left conveys the same information as the treemap on the previous tab.
                      It presents insights into both the size and the development of vendors.
                      The size of the vendors is presented on the x axis. The larger a vendor, the more it is positioned
                      to the right. On the y-axis you find the development of sales since the start of 2021.
                      The calculation is done as follows. All the weeks of data collection are split up into
                      two parts. Next, the average weekly revenues are calculated for both partitions and compared
                      to get the percentual sales change. The blue dots are related to Agartha and the orange dots 
                      to Cannazon
              
                      </DialogContentText>
                      
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfoScatterplot} color="primary">
                        Close
                      </Button>
                    </DialogActions>
      
                    </Dialog>  
                    <Grid item xs={12}>
                        <Button style={MyTheme.palette.darkmarketLightOrange}></Button>
                        &nbsp; Agartha
                        </Grid>
                        
                        <Grid item xs={12}>
                        <Button style={MyTheme.palette.agarthaMiddleBlue}></Button>
                        &nbsp; Cannazon 
                        </Grid>
                    </Grid>
              
               </Grid>
            : <div></div>}
            

       
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




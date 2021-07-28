import React, { Component,useEffect, useState } from 'react';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Line, Bar } from "react-chartjs-2";
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import { useHistory,Link  } from 'react-router-dom';
import Divider from '@material-ui/core/Divider';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';
import Video from '../MO.mp4'
import VideoPlayer from 'react-video-js-player'
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import MessageIcon from '@material-ui/icons/Message';
import Comments from "./Comments";
import commentBox from 'commentbox.io';
import DialogActions from '@material-ui/core/DialogActions';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Tour from 'reactour'
import { useLocation } from 'react-router-dom';
import Box from '@material-ui/core/Box';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';


// Set design configurations
const useStyles = makeStyles((theme) => ({
  palette: {
    primary: 'red'
  },
  gridBorder: {
    border: "1px solid #1092dd",
    borderRadius: 16,
    height: "450px",
    
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
  }
}));









const Product = () => {

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
                setTourOpen(true)
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
                 Additionally, clicking in the top right corner allows you to create a mindmap that only you can see, keeping track of
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
  
  const classes = useStyles();


  // Theme is defined to change text type if the user clicks on a drug category
  const theme = createMuiTheme({
    activeItem: {
    color:'#1092dd',
    textAlign: "center"
    
  },
  nonActiveItem: {
    fontWeight:'normal',
    textAlign: "center"
  },})


    // Set useStates. Most are defined twice, because there are 2 graphs 
    const [open, setOpen] = useState(false);
    const [openInfo, setOpenInfo] = useState(false);
    const [openComments, setOpenComments] = useState(false);
    const [productData, setProductData] = useState({});
    const [productDataMarket, setProductDataMarket] = useState({});
    const [productDataSliceLeft, setProductDataSliceLeft] = useState({});
    const [productDataSliceRight, setProductDataSliceRight] = useState({});
    const [allCategories, setAllCategories] = useState({});
    const [allCategoriesTypesData,setAllCategoriesTypesData] = useState({});
    const [allCategoriesTypesSlice,setAllCategoriesTypesSlice] = useState({});
    const [highlighted, setHighlighted] = useState('');
    const [weeklySales, setWeeklySales] = useState({});
    const [weeklySalesSliceLeft, setWeeklySalesSliceLeft] = useState({});
    const [weeklySalesSliceRight, setWeeklySalesSliceRight] = useState({});
    const [allCountries, setAllCountries] = useState({});
    const [countryNameLeft, setCountryNameLeft] = useState({});
    const [countryNameRight, setCountryNameRight] = useState({});
    const [uniqueMarkets, setUniqueMarkets] = useState([]);
    const [selectedMarket, setSelectedMarket] = useState('');
    const [selectedMarketData, setSelectedMarketData] = useState('');
    const [loaded, setLoaded] = useState(false);
    const [openSublist, setOpenSublist] = useState(false);
    const [tourOpen, setTourOpen] = useState(false);
  
  
  // Load data
  useEffect( async() => {
        
      const results = await axios.get('http://0.0.0.0:4000/productpage');
      setUniqueMarkets(Object.keys(results.data[0]))
      setSelectedMarket('All markets')

      setProductData(results.data[0])
      setProductDataMarket(results.data[0]['All markets'])
      setProductDataSliceLeft(results.data[0]['All markets']['United States'])
      setProductDataSliceRight(results.data[0]['All markets']['Netherlands'])
      setAllCountries(Object.keys(results.data[0]['All markets']))
      setWeeklySales(results.data[1])
      setWeeklySalesSliceLeft(results.data[1]['United States'])
      setWeeklySalesSliceRight(results.data[1]['Netherlands'])
      setAllCategories(results.data[2])
      setAllCategoriesTypesData(results.data[4])
      for (const [category, drugs] of Object.entries(results.data[4])){
        setAllCategoriesTypesSlice(drugs)
        break
      }
      var comment = commentBox('5753003650842624-proj')
      setCountryNameLeft('United States')
      setCountryNameRight('Netherlands')
      setLoaded(true)

   
    }, []) 

    // This function transforms the input data in such a way that it can be sent to the charts
    const productLineFunction = (dataToUse, maxYvalue) => {
      var allData = []
      //var colours = ['rgb(47,75,124)','rgb(102,81,145)',"rgb(0,63,92)", 'rgb(160,81,149)', 'rgb(212,80,135)','rgb(249,93,106)', 'rgb(255,124,67)', 'rgb(255,166,0)' ]
      var colours = [ 'rgb(209, 99, 230)', 'rgb(184, 0, 88)', 'rgb(0, 140, 249)', 'rgb(0, 110, 0)', 'rgb(0, 187, 173)', 'rgb(235, 172, 35)', 'rgb(89, 84, 214)']
      //xgfs_normal12 = [(235, 172, 35), (184, 0, 88), (0, 140, 249), (0, 110, 0), (0, 187, 173), (209, 99, 230), (178, 69, 2), (255, 146, 135), (89, 84, 214), (0, 198, 248), (135, 133, 0), (0, 167, 108), (189, 189, 189)]

      var colourCounter = 0
      var max = 0
      // Determine the max height of the chart
      for (const [week, sales] of Object.entries(maxYvalue)){
        if (sales > max){
          max = sales
        }
      }

      for (const [category, weeklyData] of Object.entries(dataToUse)){       
        allData.push(
          {
            label: category,
            data: Object.values(weeklyData),
            fill: true,
            backgroundColor: colours[colourCounter],
            borderColor: colours[colourCounter]
          })
          colourCounter += 1
      }

      

      for (const [category, weeklyData] of Object.entries(dataToUse)){
        console.log(weeklyData)
        var timestamp = Object.keys(weeklyData)
        console.log(timestamp)
        break
    }

    console.log(max)
    

      return ([{
        labels: timestamp,
        datasets:allData
      },max])
    }

    // Settings for the marketplace selector box
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




    // Function to handle when the left country selector is changed
    const handleChangeLeft = (event) => {
      setProductDataSliceLeft(productDataMarket[event.target.value])
      setWeeklySalesSliceLeft(weeklySales[event.target.value])
      setCountryNameLeft(event.target.value)

    }
    // Function to handle when the right country selector is changed
    const handleChangeRight = (event) => {
      setProductDataSliceRight(productDataMarket[event.target.value])
      setWeeklySalesSliceRight(weeklySales[event.target.value])
      setCountryNameRight(event.target.value)

    }

    // Function to handle when the marketplace selector is changed
    const handleChange = (event) => {
      var dataToLoop = event.target.value
      setSelectedMarket(dataToLoop)
      setProductDataMarket(productData[dataToLoop])
      // Based on the different market, also adapt the 2 graphs
      console.log(productData[dataToLoop])
      setProductDataSliceLeft(productData[dataToLoop][countryNameLeft])
      setWeeklySalesSliceLeft(weeklySales[countryNameLeft])

      setProductDataSliceRight(productData[dataToLoop][countryNameRight])
      setWeeklySalesSliceRight(weeklySales[countryNameRight])
    };


    // Functions to open/close information sections
    const handleClickOpenComments = () => {
      setOpenComments(true);
    };
    const handleCloseComments = (event) => {
      setOpenComments(false);
    };
    const handleClickOpen = () => {
      setOpen(true);
    };
  const handleClose = (event) => {
      setOpen(false);
    };
  const handleCloseInfo = (event) => {
    setOpenInfo(false);
  };
  const handleOpenInfo = () => {
    setOpenInfo(true);
  };




    if (loaded){
      runIt()
      console.log(allCategoriesTypesSlice)

    return (
     <div>
       <Grid className={classes.buttons} item xs={12}>
            <br></br>
              <br></br>
              <br></br>
              <br></br>
              
              <div ><font size="3">Investigate how the sales per drug category have developed</font></div>
              <Button>
                {/* VIDEO SECTION */} 
              <OndemandVideoIcon style={{color:'#FF6700', fontSize:30}} onClick={handleClickOpen} ></OndemandVideoIcon>
        </Button>
        <Dialog
                        open={open}
                        onClose={handleClose}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"lg"}
                    >
                      
                        <VideoPlayer src={Video} width="720" height="420"></VideoPlayer>
                        <DialogActions>
                      <Button onClick={handleClose} color="primary">
                        Close
                      </Button>
                      
                    </DialogActions>
                        
                    </Dialog>
                    <Button className="commentButton">
                        <MessageIcon style={{color:'#FF6700', fontSize:30}} onClick={handleClickOpenComments} ></MessageIcon>
                   </Button> 
                  {/* COMMENTS SECTION */} 
                   <Dialog 
                        open={openComments}
                        onClose={handleCloseComments}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"md"}
                        fullWidth = {true}
                    > 
                      
                        <Comments />
                        
                    </Dialog>     
  
            </Grid>
            {/* COUNTRY LEFT SELECTOR SECTION */} 
       <Grid container direction="row" justify="center" alignItems="center" spacing={2}>    
            <Grid className={classes.buttons} item xs={5} align="center">
                <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-simple">Country</InputLabel>
                <Select
                  native
                  value={countryNameLeft}
                  onChange={handleChangeLeft}
                  inputProps={{
                    name: 'age',
                    id: 'age-native-simple',
                  }}
                > {allCountries.map((country) => (
                  <option value={country}>{country}</option>
                )

                )}

                </Select>
                
       </FormControl>
       &nbsp;&nbsp;&nbsp;
       
      </Grid>

      {/* INFORMATION SECTION */} 
      <Grid item xs={1}>
              <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:50}} onClick={handleOpenInfo} />
                </Button>
                  <Dialog
                        open={openInfo}
                        onClose={handleCloseInfo}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      Drug categories
                    </DialogTitle>
                    <DialogContent>
                    <DialogContentText>
                      This page presents you with the development of sales per drug category, giving you the ability compare countries and markets.
                      <b> Be aware!</b> The reported revenue are heavily dependend on several assumption that were made.
                      Therefore it is adviced to carefully read the explanation on the calculation below. The calculation is done differently for 
                      each market since they provide different levels of data maturity
                      </DialogContentText>
                      <DialogContentText>
                      <b>Cannazon:</b> reviews on this marketplace include information on the product that is bought and the amount that is spent by the buyer.
                      Therefore, adding all of these amounts together gives a lower bound for the sales of this market. It is a lower bound since not every
                      buyer leaves a review. Since data on all the products has also been collected, it is known where the products are sent from. By connecting
                      this shipping location to the amount that is spent by a buyer, an estimation of the sales can be made.
                      </DialogContentText>
                      <DialogContentText>
                      <b>Agartha:</b> reviews on this marketplace rarely provide information about the product that is bought. Additionally, this market
                      also sells other goods, not related to drugs. Therefore, it is not known with certainty whether a review is related to a drugs-related
                      product. To get an estimation of the drug/non-drug review ratio, all the reviews within a certain week that contain a product name
                      were analysed. This ratio was afterwards used to estimate how many of the reviews without any text were drug related. None of the reviews
                      mentioned the price that was spent. Therefore the following calculation was done. For every vendor, all the products that he offered were
                      categorized under the right product group. It has been assumed that the reviews are evenly distributed over the products of a vendor. As
                      a result, the assigned reviews per category can be multiplied by the average price of the products within that category to get an estimate
                      of the revenue. <br></br> For example, vendor X has 10 reviews in week 1. The calculated drug/non-drug ratio for that week is 0.8. This means that 8 
                      of his reviews are approximately devoted to drugs. It is known that 4 products are offered by vendor X, 2 of them are Opiates shipped from
                      the Netherlands with an average price of €100 and 2 of them are Stimulants shipped from Germany with an average price of €50. Therefore, the
                      approximation of his sales for the category Stimulants are 4 reviews * €100 = €400, while for the category Opiates the approximation is 
                      4 reviews * €50 = €200. Admittedly, this estimation is worse than from Cannazon, but the best that can be done with the provided data of the 
                      marketplace.
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button autoFocus onClick={handleCloseInfo} color="primary">
                        Close
                      </Button>
                    </DialogActions>
      
                    </Dialog>  
      </Grid>
      {/* MARKETPLACE SELECTOR SECTION */} 
      <Grid  item xs={1} align="center">
      <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-simple">Markets</InputLabel>
                <Select
                  native
                  value={selectedMarket}
                  onChange={handleChange}
                  inputProps={{
                    name: 'age',
                    id: 'age-native-simple',
                  }}
                > {uniqueMarkets.map((market) => (
                  <option value={market}>{market}</option>
                )

                )}

                </Select>
                
       </FormControl>
       {/* COUNTRY RIGHT SELECOTR SECTION */} 
                    </Grid> 
      <Grid className={classes.buttons} item xs={5} align="center">
                <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-simple">Country</InputLabel>
                <Select
                  native
                  value={countryNameRight}
                  onChange={handleChangeRight}
                  inputProps={{
                    name: 'age',
                    id: 'age-native-simple',
                  }}
                > {allCountries.map((country) => (
                  <option value={country}>{country}</option>
                )

                )}

                </Select>
                
       </FormControl>
       &nbsp;&nbsp;&nbsp;
       
      </Grid>
      </Grid>

      {/* LEFT AREA CHART SECTION */} 
      <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
          <Grid item xs={6} align="center">
          <Line 
            data={productLineFunction(productDataSliceLeft,weeklySalesSliceLeft)[0]}
              
              
          
            options = {{
              
                title: {
                    display: true,
                    text: `Products that are shipped from ${countryNameLeft}`,
                  
  
            },
              scales: {yAxes: [{
                ticks:{               
                  suggestedMax: Math.max.apply(Math, [ productLineFunction(productDataSliceLeft,weeklySalesSliceLeft)[1],  productLineFunction(productDataSliceRight,weeklySalesSliceRight)[1]]),
                  beginAtZero: true,
                  callback: function(value, index, values) {
                    if(parseInt(value) >= 1000){
                      return '€' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                    } else {
                      return '€' + value;
                    }
                  }

                  },
                  stacked: true,
                  scaleLabel: {
                    display: true,
                    labelString: 'Estimated revenue'
                   }, 
                 
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: 'Date in weeks'
                  }
                }],
              }     
            }}
            />
           
           
            </Grid>
           
           
          {/* RIGHT AREA CHART SECTION */} 
            <Grid item xs={6} align="center">
          <Line 
            data={productLineFunction(productDataSliceRight,weeklySalesSliceRight)[0]}
              
            options = {{
              title: {
                display: true,
                text: `Products that are shipped from ${countryNameRight}`,
              

              },
              scales: {
                yAxes: [{
                  ticks:{
                    suggestedMax: Math.max.apply(Math, [ productLineFunction(productDataSliceLeft,weeklySalesSliceLeft)[1],  productLineFunction(productDataSliceRight,weeklySalesSliceRight)[1]]),
                    beginAtZero: true,
                    callback: function(value, index, values) {
                      if(parseInt(value) >= 1000){
                        return '€' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                      } else {
                        return '€' + value;
                      }
                    }
                  },
                  stacked: true,
                  scaleLabel: {
                    display: true,
                    labelString: 'Estimated revenue'
                  }  
                    
                  
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: 'Date in weeks'
                  }
                }],
              }     
            }}
            />
           
           
            </Grid>
            </Grid>

            {/* TABLE SECTION */} 
            <Grid container direction="row"  spacing={2}>
            <MuiThemeProvider theme={theme}>
              <Grid item xs={4}></Grid>
            <Grid item xs={2} align="center">
                 <br></br>
                       <Typography variant="subtitle2"  align="center">
                           Drug categories
                       </Typography>
                       <Divider />
                      
               <List style={{height: "170px", overflow: 'auto'}}>
               {allCategories.map((category) => (
                        <div>
                         <ListItem button onClick={() => {setHighlighted(category);setAllCategoriesTypesSlice(Object.values(allCategoriesTypesData[category])); setOpenSublist(true)}}>

                         <ListItemText style={highlighted === category ? theme.activeItem : theme.nonActiveItem} primary={category} />
                         
                       </ListItem>
                       <Divider />
                       </div>
                         ))}
     
               </List>
               </Grid>
               
            
            <Grid item xs={2} align="center">
                 <br></br>
                       <Typography variant="subtitle2"  align="center">
                           Drugs belonging to category
                       </Typography>
                       <Divider />
                       {openSublist ? 
               <List style={{height: "165px", overflow: 'auto'}}>
               {allCategoriesTypesSlice.map((category) => (
                        <div>
                         <ListItem >

                         <ListItemText style={theme.nonActiveitem} primary={category} />
                         
                       </ListItem>
                       <Divider />
                       </div>
                         ))}
                         </List>
                         : <div></div>}
     
     
               
               </Grid>
               <Grid item xs={4}></Grid>
               </MuiThemeProvider>
               
            </Grid>
            <Tour
                    steps={steps}
                    isOpen={tourOpen}
                    onRequestClose={() => setTourOpen(false)}
                    startAt={19}
                    rounded={10}
                     />

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

  export default Product;
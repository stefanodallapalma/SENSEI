// This function is responsible for creating the entire 'how' page within the dashboard
// It does so by defining the various functionalities + importing the network functionality

// Import necessary packages and scripts
import React,{ useState, useRef, useEffect, useCallback,PureComponent } from "react";
import { Line, Bar } from "react-chartjs-2";
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Network from './Network'
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';
import Video from '../MO.mp4'
import VideoPlayer from 'react-video-js-player'
import Dialog from '@material-ui/core/Dialog';
import MessageIcon from '@material-ui/icons/Message';
import Comments from "./Comments";
import commentBox from 'commentbox.io';
import DialogActions from '@material-ui/core/DialogActions';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';
import Input from '@material-ui/core/Input';
import PersonIcon from '@material-ui/icons/Person';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { useHistory,Link  } from 'react-router-dom';
import MyTheme from './MyTheme'
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import Tour from 'reactour'
import { useLocation } from 'react-router-dom';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import pattern from 'patternomaly';


// Define layout settings that will be used on this page
const useStyles = makeStyles((theme) => ({
  palette: {
    primary: 'red'
  },
  gridBorder: {
    border: "1px solid #1092dd",
    borderRadius: 16,
    height: "470px",
    padding: 10
    
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
    minWidth : 500,
  },
  buttons: {
    display: 'flex',
    justifyContent: "center",
    alignItems:"center"
  },
  
}));


// Create the function that will be exported. MO stands for modus operandi
const MO = () => {

  // Define the useStates that will be used
  const classes = useStyles();
  // UseStates responsible for opening/closing the various tabs on the page
  const [open, setOpen] = useState(false);
  const [openShipping, setOpenShipping] = useState(false);
  const [openComments, setOpenComments] = useState(false);
  const [openTargeted, setOpenTargeted] = useState(false);
  const [openSpecialist, setOpenSpecialist] = useState(false);
  const [openNetwork, setOpenNetwork] = useState(false);
  const [openGroup, setOpenGroup] = useState(false);
  const [timestamps, setTimestamps] = useState([]);
  // Usestates for the distributor/ end consumer page
  const [distributorData, setDistributorData] = useState({});
  const [distributorDataSliceLeft, setDistributorDataSliceLeft] = useState({});
  const [distributorDataSliceRight, setDistributorDataSliceRight] = useState({});
  // UseStates that house what countries are currently selected
  const [allCountries, setAllCountries] = useState({});
  const [countryNameLeft, setCountryNameLeft] = useState({});
  const [countryNameRight, setCountryNameRight] = useState({});
  const [dataToRender, setDataToRender] = useState();
  // UseStates for individual/group functionality
  const [individualData, setIndividualData] = useState();
  const [individualDataSliceLeft, setIndividualDataSliceLeft] = useState({});
  const [individualDataSliceRight, setIndividualDataSliceRight] = useState({});
  const [categoryRendered, setCategoryRendered] = useState({});
  // UseStates for the name lists at the bottom of the page
  const [renderListTargetedLeft, setRenderListTargetedLeft ] = useState(false);
  const [renderListTargetedRight, setRenderListTargetedRight ] = useState(false);
  const [renderListCollaborationLeft,setRenderListCollaborationLeft] = useState(false);
  const [renderListCollaborationRight,setRenderListCollaborationRight] = useState(false);
  // UseStates that save the name of the bar that is clicked by the user
  const [barchartClickMarketLeft, setBarchartClickMarketLeft] = useState();
  const [barchartClickTypeLeft, setBarchartClickTypeLeft] = useState();
  const [barchartClickMarketRight, setBarchartClickMarketRight] = useState();
  const [barchartClickTypeRight, setBarchartClickTypeRight] = useState();
  const [vendorOperationalTab, setVendorOperationalTab] = useState();
  // UseStates for specialist/generalist segment
  const [specialistGeneralistData, setSpecialistGeneralistData] = useState({});
  const [specialistGeneralistDataSliceLeft, setSpecialistGeneralistDataSliceLeft] = useState({});
  const [specialistGeneralistDataSliceRight, setSpecialistGeneralistDataSliceRight] = useState({});
  const [renderListSpecialistLeft,setRenderListSpecialistLeft] = useState(false);
  const [renderListSpecialistRight,setRenderListSpecialistRight] = useState(false);
  // UseStates for the required height of the y-axis.
  // Is done for both graphs on the page, the max value will be used for both graphs, so that they will be equal
  const [yAxisHeight, setYAxisHeight] = useState({});
  const [yAxisHeightLeft, setYAxisHeightLeft] = useState({});
  const [yAxisHeightRight, setYAxisHeightRight] = useState({});
  const [countryYAxis, setCountryYAxis] = useState({});
  const [countryYAxisLeft, setCountryYAxisLeft] = useState({});
  const [countryYAxisRight, setCountryYAxisRight] = useState({});
  const [uniqueMarkets, setUniqueMarkets] = useState([]);
  const [selectedMarkets, setSelectedMarkets] = useState([]);
  const [countryData, setCountryData] = useState([]);
  const [countryDataMarket, setCountryDataMarket] = useState([]);
  const [countryMarkets, setCountryMarkets] = useState([]);
  const [selectedCountryMarkets, setSelectedCountryMarkets] = useState([]);
  const [countryDataMarketsSliceLeft, setCountryDataMarketsSliceLeft] = useState([]);
  const [countryDataMarketsSliceRight, setCountryDataMarketsSliceRight] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [tourOpen, setTourOpen] = useState(false);
  const [showResultsTargetedCustomer, setShowResultsTargetedCustomer] = useState(false)
  const [showResultsTargetedMarkets, setShowResultsTargetedMarkets] = useState(false)
  const [showResultsCollaboration, setShowResultsCollaboration] = useState(false);
  const [showResultsSpecialist, setShowResultsSpecialist] = useState(false);
  const [showResultsShipping, setShowResultsShipping] = useState(false);

  // All the buttons
  const [button1, setButton1] = useState(false);
  const [button2, setButton2] = useState(false);
  const [button3, setButton3] = useState(false);
  const [button4, setButton4] = useState(false);
  const [button5, setButton5] = useState(false);

 // Import all the data from the FLASK application
  useEffect( async() => {
    const all_data = await axios.get("http://0.0.0.0:4000/product");
    setTimestamps(all_data.data[0])
    setDistributorData(all_data.data[1])
    setDistributorDataSliceLeft(all_data.data[1]['United States'])
    setDistributorDataSliceRight(all_data.data[1]['Netherlands'])
    setYAxisHeight(all_data.data[2])
    setYAxisHeightLeft(all_data.data[2]['United States'])
    setYAxisHeightRight(all_data.data[2]['Netherlands'])
    setCountryNameLeft('United States')
    setCountryNameRight('Netherlands')
    setAllCountries(Object.keys(all_data.data[1]))
    setUniqueMarkets(all_data.data[3])
    setSelectedMarkets(all_data.data[3])
   

    const individual_data = await axios.get("http://0.0.0.0:4000/nlp");
    setIndividualData(individual_data.data[0])
    setIndividualDataSliceLeft(individual_data.data[0]['United States'])
    setIndividualDataSliceRight(individual_data.data[0]['Netherlands'])
    

    const specialistData = await axios.get("http://0.0.0.0:4000/productpage");
    setSpecialistGeneralistData(specialistData.data[5])
    setSpecialistGeneralistDataSliceLeft(specialistData.data[5]['United States'])
    setSpecialistGeneralistDataSliceRight(specialistData.data[5]['Netherlands'])

    const countriesData = await axios.get("http://0.0.0.0:4000/operational");
    setCountryData(countriesData.data[7])
    setCountryDataMarket(countriesData.data[7]['All markets'])
    setCountryMarkets(Object.keys(countriesData.data[7]))
    setSelectedCountryMarkets('All markets')
    setCountryDataMarketsSliceLeft(countriesData.data[7]['All markets']['United States'])
    setCountryDataMarketsSliceRight(countriesData.data[7]['All markets']['Netherlands'])
    setCountryYAxis(countriesData.data[1])
    setCountryYAxisLeft(countriesData.data[1]['United States'])
    setCountryYAxisRight(countriesData.data[1]['Netherlands'])
    setLoaded(true);

  }, [])
  // Connect to the commentbox extension to allow for the display of the comments
  useEffect( async() => {
    var comment = commentBox('5753003650842624-proj')
  })
  // Opens the comment section
  const handleClickOpenComments = () => {
    setOpenComments(true);
  };
  // Closes the comment section
  const handleCloseComments = (event) => {
    setOpenComments(false);
  };

  // These functions define whether the information sections of the relative section will be openened/closed
  const handleClickOpenTargeted = () => {
    setOpenTargeted(true);
  };
  const handleCloseTargeted = (event) => {
    setOpenTargeted(false);
  };
  const handleClickOpenGroup = () => {
    setOpenGroup(true);
  };
  const handleCloseGroup = (event) => {
    setOpenGroup(false);
  };
  const handleClickOpenSpecialist = () => {
    setOpenSpecialist(true);
  };
  const handleCloseSpecialist = (event) => {
    setOpenSpecialist(false);
  };
  const handleClickOpenShipping = () => {
    setOpenShipping(true);
  };
  const handleCloseShipping = (event) => {
    setOpenShipping(false);
  };
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClickOpenNetwork = () => {
    setOpenNetwork(true);
  };
  const handleCloseNetwork = (event) => {
    setOpenNetwork(false);
  };
const handleClose = (event) => {
    setOpen(false);
  };


  // This function is used to make sure that the tour functionality can be used
  // Once the page loads, it detects whether anything is present in the location.state
  // If that is the case, the tour is set to true
  // It will be called further on in the script
    const location = useLocation();
    const history = useHistory();
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
          // These are all the various steps from the tour. All of them have to be defined, otherwise the presented
          // amount of total steps will not be true.
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


if (loaded){

  // This the function that checks whether the tour has to be activated or not  
  runIt()

  console.log(countryMarkets)
  // Function that handles the change within the left graph if a new country is selected
  const handleChangeLeft = (event) => {
    setDistributorDataSliceLeft(distributorData[event.target.value])
    setIndividualDataSliceLeft(individualData[event.target.value])
    setSpecialistGeneralistDataSliceLeft(specialistGeneralistData[event.target.value])
    setCountryDataMarketsSliceLeft(countryDataMarket[event.target.value])
    setCountryNameLeft(event.target.value)
    setYAxisHeightLeft(yAxisHeight[event.target.value])
    setCountryYAxisLeft(countryYAxis[event.target.value])
    graphDataSize(distributorDataSliceLeft,yAxisHeight[event.target.value],selectedMarkets)
    graphDataSize(individualDataSliceLeft,yAxisHeight[event.target.value],selectedMarkets)
   // processCountryData(countryDataMarket[event.target.value])

    
  }
 // Function that handles the change within the right graph if a new country is selected
  const handleChangeRight = (event) => {
    setDistributorDataSliceRight(distributorData[event.target.value])
    setIndividualDataSliceRight(individualData[event.target.value])
    setSpecialistGeneralistDataSliceRight(specialistGeneralistData[event.target.value])
    setCountryDataMarketsSliceRight(countryDataMarket[event.target.value])
    setCountryNameRight(event.target.value)
    setYAxisHeightRight(yAxisHeight[event.target.value])
    setCountryYAxisRight(countryYAxis[event.target.value])
    graphDataSize(distributorDataSliceRight,yAxisHeight[event.target.value],selectedMarkets)
    graphDataSize(individualDataSliceRight,yAxisHeight[event.target.value],selectedMarkets)
    //processCountryData(countryDataMarket[event.target.value])
    
  }

  // Functions for the select box
  const handleChange = (event) => {
    var dataToLoop = event.target.value
    setSelectedMarkets(dataToLoop)
    // Set 'shipping' tab useStates
    setSelectedCountryMarkets(dataToLoop)
    setCountryDataMarket(countryData[dataToLoop])

  };

  // This function defines the colours of the bars of the various marketplaces
  // NEW ADDITIONS SHOULD BE MADE IF MORE MARKETS GET ADDED!
  const helperColourSize = (type,market) => {
    // Distributor/retailer colours agartha
    if (type === 'Distributor' && market === 'agartha'){
      return ("#005073")
    } if (type === 'Both' && market === 'agartha'){
      return("#189ad3")
    } if (type === "End user" && market === 'agartha'){
      return ("#71c7ec")
    }

    // Distributor/retailer colours cannazon
    if (type === 'Distributor' && market === 'cannazon'){
      return ("#ff6600")
    } if (type === "End user" && market === 'cannazon'){
      return ("#ffaf7a")
    } if (type === 'Both' && market === 'cannazon'){
      return("#ff8b3d")
    }

    // Individual/group colours Agartha
    if (type === 'Group' && market === 'agartha'){
      return ("#005073")
    } if (type === "Individual" && market === 'agartha'){
      return ("#189ad3")
    } if (type === 'Unknown' && market === 'agartha'){
      return("#71c7ec")
    }
    // Individual/group colours cannazon
    if (type === 'Group' && market === 'cannazon'){
      return ("#ff6600")
    } if (type === "Individual" && market === 'cannazon'){
      return ("#ff8b3d")
    } if (type === 'Unknown' && market === 'cannazon'){
      return("#ffaf7a")
    }

    // Specialist/generalist colours Agartha
    if (type === 'Specialist' && market === 'agartha'){
      return ("#005073")
    } if (type === 'Generalist' && market === 'agartha'){
      return("#71c7ec")
    }
    // Specialist/generalist colours cannazon
    if (type === 'Specialist' && market === 'cannazon'){
      return ("#ff6600")
    } if (type === 'Generalist' && market === 'cannazon'){
      return("#ffaf7a")
    }
  }

  
  // This function supports the 'GraphDataSize' function
    const helperGraphDataSize = (dictionary) => {
      var output = {"agartha": [], 'darkmarket': [], 'cannazon': []}
      var temp = {"agartha": [], 'darkmarket': [], 'cannazon': []}

      for (const [timestamp, data] of Object.entries(dictionary)){
        var all_market_for_timestamp = Object.keys(data)
        for (const [market, count] of Object.entries(temp)){
          if (!(all_market_for_timestamp.includes(market))) {
            output[market].push(0)
          } else{
            for (const [presentMarket, vendors] of Object.entries(data)){
              if (presentMarket === market){
                output[market].push(vendors.length)
                
              }
            }
          }
        }
      }
      
      return(output)

    }

    
    // This function alters the input data from the useEffect in such a way that it is accepted by the graphs
    const graphDataSize = (dataToUse,maxYValue,marketsToDisplay) => {
      var finalData = {}
      var allData = []
      //Determine the required height of the y-axis
      var max = 0
      console.log(maxYValue)
      for (const [market, dates] of Object.entries(maxYValue)){
        if (marketsToDisplay.includes(market)){
          for (const [date, count] of Object.entries(dates)){
            if (count > max){
              max = count
            }
          }
        }
      }

      for (const [category,timestamps] of Object.entries(dataToUse)){
        var formatedData = helperGraphDataSize(timestamps)
        console.log(formatedData)
        for (const [market, data] of Object.entries(formatedData)){
          if (market === 'agartha' && marketsToDisplay.includes('agartha')){

            allData.push({
              label: market + "- " + category ,
              backgroundColor: helperColourSize(category,market),
              borderColor: helperColourSize(category,market),
              borderWidth: 1,
              stack: 1,
              hoverBackgroundColor: helperColourSize(category,market),
              hoverBorderColor: helperColourSize(category,market),
              data: data
          })}
          if (market === 'cannazon' && marketsToDisplay.includes('cannazon')){

            allData.push({
              label: market + "- " + category ,
              backgroundColor: helperColourSize(category,market),
              borderColor: helperColourSize(category,market),
              borderWidth: 1,
              stack: 2,
              hoverBackgroundColor: helperColourSize(category,market),
              hoverBorderColor: helperColourSize(category,market),
              data: data
          })
          }
          
        }
      }
           
      return ([{
        labels : timestamps,
        datasets: allData
      },max])
    }

    // This functions both handles the colour change when a new tab is clicked and the content that is presented
    const buttonChange = (number) => {
      if (number === 1){
        setButton1(true)
        setButton2(false)
        setButton3(false)
        setButton4(false)
        setButton5(false)
      }
      if (number === 2){
        setButton1(false)
        setButton2(true)
        setButton3(false)
        setButton4(false)
        setButton5(false)
      }
      if (number === 3){
        setButton1(false)
        setButton2(false)
        setButton3(true)
        setButton4(false)
        setButton5(false)
      }
      if (number === 4){
        setButton1(false)
        setButton2(false)
        setButton3(false)
        setButton4(true)
        setButton5(false)
      }
      if (number === 5){
        setButton1(false)
        setButton2(false)
        setButton3(false)
        setButton4(false)
        setButton5(true)
      }
    }

    // This function helps output a list of vendors that belong to the category that the user has clicked on
    const  handleChartClickHelper = (clickedOnType,clickedOnMarket,leftOrRight,type, slice,individualSlice, generalistData) => {

      if (type === 'targeted markets'){
        const allVendors = []

        // Take all vendornames that belong to the category that is clicked on
        for (const [category, timestamps] of Object.entries(slice)){
          for (const [timestamp, markets] of Object.entries(timestamps)){
            for (const [market, vendor] of Object.entries(markets)){
              if (category === clickedOnType && market === clickedOnMarket){
                if (!(allVendors.includes(vendor))){
                  allVendors.push(vendor)
                  
                }
            }
            }
          }
        }
  
        var finalList = []
        for (const partList of allVendors){
          for (const item of partList){
            if (!(finalList.includes(item))){
              finalList.push(item)
            }
          }
        }
        
        if(leftOrRight == 'left'){
          setRenderListTargetedLeft(finalList)
        }
        if(leftOrRight == 'right'){
          setRenderListTargetedRight(finalList)
        }
        
        return(finalList)

      } if (type === 'collaboration'){
        const allVendors = []
      

        // Take all vendornames that belong to the category that is clicked on
        for (const [category, timestamps] of Object.entries(individualSlice)){
          for (const [timestamp, markets] of Object.entries(timestamps)){
            for (const [market, vendor] of Object.entries(markets)){
              if (category === clickedOnType && market === clickedOnMarket){
                if (!(allVendors.includes(vendor))){
                  allVendors.push(vendor)
                  
                }
            }
            
            }
          }
         
        }
  
        var finalList = []
        for (const partList of allVendors){
          for (const item of partList){
            if (!(finalList.includes(item))){
              finalList.push(item)
            }
          }
        }
        if(leftOrRight == 'left'){
          setRenderListCollaborationLeft(finalList)
        }
        if(leftOrRight == 'right'){
          setRenderListCollaborationRight(finalList)
        }
        return(finalList)}

        if (type === 'specialistGeneralist'){
          const allVendors = []
        
  
          // Take all vendornames that belong to the category that is clicked on
          for (const [category, timestamps] of Object.entries(generalistData)){
            for (const [timestamp, markets] of Object.entries(timestamps)){
              for (const [market, vendor] of Object.entries(markets)){
                if (category === clickedOnType && market === clickedOnMarket){
                  if (!(allVendors.includes(vendor))){
                    allVendors.push(vendor)
                    
                  }
              }
              
              }
            }
           
          }
    
          var finalList = []
          for (const partList of allVendors){
            for (const item of partList){
              if (!(finalList.includes(item))){
                finalList.push(item)
              }
            }
          }
          if(leftOrRight == 'left'){
            setRenderListSpecialistLeft(finalList)
          }
          if(leftOrRight == 'right'){
            setRenderListSpecialistRight(finalList)
          }
  
        
        return(finalList)
      }
     

    }

    
   // This function uses last function and defines what list is displayed for the left chart
    function handleChartClickLeft(dataset,type) {
      
      if (dataset.length > 0){
        const clickedOnCategory = dataset[0]._model.datasetLabel
        const clickedOnMarket = clickedOnCategory.split('-')[0]
        const clickedOnType = clickedOnCategory.split('- ')[1]
        setBarchartClickMarketLeft(clickedOnMarket)
        setBarchartClickTypeLeft(clickedOnType)
        handleChartClickHelper(clickedOnType,clickedOnMarket,'left',type,distributorDataSliceLeft,individualDataSliceLeft,specialistGeneralistDataSliceLeft )
      }
      
      

    }
    // Same as above, but for the right chart
    function handleChartClickRight(dataset,type) {
      
      if (dataset.length > 0){
        const clickedOnCategory = dataset[0]._model.datasetLabel
        const clickedOnMarket = clickedOnCategory.split('-')[0]
        const clickedOnType = clickedOnCategory.split('- ')[1]
        setBarchartClickMarketRight(clickedOnMarket)
        setBarchartClickTypeRight(clickedOnType)
        handleChartClickHelper(clickedOnType,clickedOnMarket,'right',type,distributorDataSliceRight,individualDataSliceRight, specialistGeneralistDataSliceRight)
      }
      
      

      

    }
    const handleVendorClick = (vendor) => {
      setVendorOperationalTab(vendor)
  }

  // Some settings for the box that appears if you want to select the markets
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

  // This function is used to transform the area chart data on the 'targeted markets' page 
  // to its right format
  const processCountryData = (dataToUse, maxYValue) => {
    //Determine the required height of the y-axis
    var max = 0
    console.log(maxYValue)
    for (const [date, count] of Object.entries(maxYValue)){
      if (count > max){
        max = count
      }
    }
      
    
    // These settings define the patterns used in the area chart
    var colours = ['#4053d3', '#ddb310']
    var patternChoice = ['dash', 'dot']
    var colourCounter = 0
    var allData = []
    for (const [category, weeks] of Object.entries(dataToUse)){
      var dataForWeeks = []
      for (const [week, vendors] of Object.entries(weeks)){
        dataForWeeks.push(vendors.length)
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

    return ([{
        labels : timestamps,
        datasets: allData
      },max])
  }




  // Settings for the charts
  const options = {
    responsive: true,
    
    legend: {
      display: false,
    },
    type: "bar",
    animation: {
      duration: 1500,
    },
    scales: {yAxes: [{
      ticks:{               
        suggestedMax: Math.max.apply(Math, [ graphDataSize(distributorDataSliceLeft,yAxisHeightLeft,selectedMarkets)[1],  graphDataSize(distributorDataSliceRight,yAxisHeightRight,selectedMarkets)[1]])
  
        },
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
        }]}
  
  };
   
   
  
    return (
        <div className="nice">
          <Grid container spacing={2}>
            
            <Grid className={classes.buttons} item xs={12}>
            <br></br>
              <br></br>
              <br></br>
              <br></br>
              
              <div ><font size="3">Investigate how vendors do business</font></div>
              <Button>
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
  
            </Grid>
    
            
       
       
     
      </Grid>

 {/* DEFINE ALL THE INFORMATION SECTIONS */}
          <Dialog
                open={openTargeted}
                onClose={handleCloseTargeted}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                fullWidth = {true}
            > 
            <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
              Targeted customers
            </DialogTitle>
            <DialogContent>
              <DialogContentText>
                This page clarifies who the vendors target with their products. They can either sell products in small batches,
                targeting end consumers, or sell products in large quantities, serving as distributors. The distinction is made
                on the price of all the products for a vendor. If all of the products of a vendor are more expensive than €1000
                he is regarded as a distributor. Otherwise, he targets end consumers. If he sells both products more and less expensive
                he belongs to the category "both". 
              </DialogContentText>
              <DialogContentText>
                Each bar represents a single market, the different shades indicate the different categories. Developments through
                time can be studied across markets and countries. Markets can be selected above this information section.
                By clicking on a bar, the vendors belonging to that category
                appear below the graph. By clicking on them you are redirected to the "who" page.
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button autoFocus onClick={handleCloseTargeted} color="primary">
                Close
              </Button>
            </DialogActions>
            </Dialog>   
            
            
            <Dialog
                  open={openNetwork}
                  onClose={handleCloseNetwork}
                  aria-labelledby="alert-dialog-title"
                  aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                  fullWidth = {true}
              > 
              <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                Network
              </DialogTitle>
              <DialogContent>
                <DialogContentText>
                  This page clarifies whether vendors are active on one or multiple markets. It allows you to check the presence
                  of vendors on markets by means of a network graph and a table. The white dots resemble the markets, the blue
                  dots are the vendors.
                </DialogContentText>
    
              </DialogContent>
              <DialogActions>
                <Button autoFocus onClick={handleCloseNetwork} color="primary">
                  Close
                </Button>
              </DialogActions>
                        
                  </Dialog>  



                  <Dialog
                          open={openGroup}
                          onClose={handleCloseGroup}
                          aria-labelledby="alert-dialog-title"
                          aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                          fullWidth = {true}
                      > 
                      <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                        Collaboration
                      </DialogTitle>
                      <DialogContent>
                        <DialogContentText>
                        The graphs on this page show the distribution of vendors that operate in a group or alone.
                        This information is extracted from the personal desciption written by most vendors on their 
                        homepage. Nouns occuring in plural form, like 'we' or 'us', imply the vendor is part of a 
                        group, whereas nouns written in singular form, like 'I', indicate that the vendor is operating 
                        alone. Admittedly, this is an estimation, but it gives an indication of the professionality of vendors.
                        </DialogContentText>
                        <DialogContentText>
                          Each bar represents a single market, the different shades indicate the different categories. Developments through
                          time can be studied across markets and countries. Markets can be selected above this information section.
                          By clicking on a bar, the vendors belonging to that category
                          appear below the graph. By clicking on them you are redirected to the "who" page.
                        </DialogContentText>
                      </DialogContent>
                      <DialogActions>
                        <Button autoFocus onClick={handleCloseGroup} color="primary">
                          Close
                        </Button>
                      </DialogActions>
        
                      </Dialog>  


              <Dialog
                                open={openSpecialist}
                                onClose={handleCloseSpecialist}
                                aria-labelledby="alert-dialog-title"
                                aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                                fullWidth = {true}
                            > 
                            <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                              Specialist/Generalist
                            </DialogTitle>
                            <DialogContent>
                              <DialogContentText>
                              This page informs you about variety of products vendors offer. The analysis is done based on the 
                              products found for a vendor. If no products are found for a vendor, he is left out of the analysis.
                              If all of his products fall within one product group, he is regarded as a specialist. Otherwise, he is regarded
                              as a generalist, offering products in a wider range of categories. All of the product categories can be found
                              on the "what" page.
                              </DialogContentText>
                              <DialogContentText>
                                Each bar represents a single market, the different shades indicate the different categories. Developments through
                                time can be studied across markets and countries. Markets can be selected above this information section.
                                By clicking on a bar, the vendors belonging to that category
                                appear below the graph. By clicking on them you are redirected to the "who" page.
                              </DialogContentText>
                            </DialogContent>
                            <DialogActions>
                              <Button autoFocus onClick={handleCloseSpecialist} color="primary">
                                Close
                              </Button>
                            </DialogActions>
              
                            </Dialog>   



                            <Dialog
                              open={openShipping}
                              onClose={handleCloseShipping}
                              aria-labelledby="alert-dialog-title"
                              aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                              fullWidth = {true}
                          > 
                          <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                            Shipping points
                          </DialogTitle>
                          <DialogContent>
                            <DialogContentText>
                              This page presents whether vendors ship from one or multiple countries. The analysis is based
                              on all the products that are found for a vendor. If products are reported to being shipped from
                              more than 1 country, he is believed to be shipping from various countries. Naturally, if only
                              1 country is found he has a single point of origin. 
                            </DialogContentText>
            
                          </DialogContent>
                          <DialogActions>
                            <Button autoFocus onClick={handleCloseShipping} color="primary">
                              Close
                            </Button>
                          </DialogActions>
            
                          </Dialog>      

 {/* CREATE ALL THE BUTTONS FOR THE TABS */}   
            <Grid container className="mobuttons"
                direction="row"
                justify="center"
                alignItems="center" spacing={2}>

            <Grid item xs="auto">
            <Grid container 
                direction="column">
            <Grid item xs='auto' align="center"  >
                   <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleClickOpenTargeted} />
                </Button>
                </Grid>
                <Grid item xs="auto">
              <Button  variant={button1 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(1);setShowResultsShipping(false); setShowResultsCollaboration(false); setShowResultsTargetedMarkets(false); setShowResultsSpecialist(false); setShowResultsTargetedCustomer(true)}}>Targeted customer</Button>
              </Grid>
            </Grid>
            </Grid>


            <Grid item xs="auto">
            <Grid container 
                direction="column">
            <Grid item xs='auto' align="center"  >
                   <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleClickOpenNetwork} />
                </Button>
                </Grid>
            <Grid  item xs='auto'   >
              <Button variant={button2 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(2);setShowResultsShipping(false); setShowResultsCollaboration(false); setShowResultsTargetedCustomer(false); setShowResultsSpecialist(false); setShowResultsTargetedMarkets(true)}} >Targeted markets</Button>
            </Grid>
            </Grid>
            </Grid>

            <Grid item xs="auto">
            <Grid container 
                direction="column">
                    <Grid item xs='auto' align="center"  >
                   <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleClickOpenSpecialist} />
                </Button>
                </Grid>
            <Grid  item xs='auto'   >
              <Button variant={button4 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(4); setShowResultsShipping(false); setShowResultsTargetedCustomer(false); setShowResultsTargetedMarkets(false); setShowResultsCollaboration(false); setShowResultsSpecialist(true)}} >Specialist/generalist</Button>
            </Grid>
            </Grid>
            </Grid>

            <Grid item xs="auto">
            <Grid container 
                direction="column">
                  <Grid item xs='auto' align="center"  >
                   <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleClickOpenShipping} />
                </Button>
                </Grid>
            <Grid  item xs='auto'   >
              <Button variant={button5 ? "contained" : "outlined"} size="small" color="primary" onClick={() => {buttonChange(5); setShowResultsTargetedCustomer(false); setShowResultsTargetedMarkets(false); setShowResultsCollaboration(false); setShowResultsSpecialist(false); setShowResultsShipping(true)}}  >Point(s) shipped from</Button>
            </Grid>
            </Grid>
            </Grid>


            <Grid item xs="auto">
            <Grid container 
                direction="column">
                  <Grid item xs='auto' align="center"  >
                   <Button>
                <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:30}} onClick={handleClickOpenGroup} />
                </Button>
                </Grid>
                <Grid  item xs='auto'   >
              <Button variant={button3 ? "contained" : "outlined"} size="small" color="primary"  onClick={() => {buttonChange(3);setShowResultsShipping(false); setShowResultsTargetedCustomer(false); setShowResultsTargetedMarkets(false); setShowResultsSpecialist(false); setShowResultsCollaboration(true)}}>Collaboration</Button>
            </Grid>
                </Grid>
            </Grid>
            


            <Grid  item xs='auto'   >
              <Button variant="disabled" size="small" color="primary"  >Payment currency</Button>
            </Grid>
            <Grid  item xs='auto'   >
              <Button variant="disabled" size="small" color="primary"  >Finished/semi-finished product</Button>
            </Grid>
            </Grid>
            <br></br>
            <br></br>

{/* /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////         */}
           
            {/* DEFINE TARGETED CUSTOMER LAYOUT */}
            {showResultsTargetedCustomer ? 
            <div>
            <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
              <Grid item xs={5} align="center">
   
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
       </Grid>



       <Grid  item xs={2} align="center">
                      <FormControl className={classes.formControl}>
                        <InputLabel id="demo-mutiple-checkbox-label">Markets</InputLabel>
                        <Select
                          labelId="demo-mutiple-checkbox-label"
                          id="demo-mutiple-checkbox"
                          multiple
                          value={selectedMarkets}
                          onChange={handleChange}
                          input={<Input />}
                          renderValue={(selected) => selected.join(', ')}
                          MenuProps={MenuProps}
                        >
                          {uniqueMarkets.map((name) => (
                            <MenuItem key={name} value={name}>
                              <Checkbox checked={selectedMarkets.indexOf(name) > -1} />
                              <ListItemText primary={name} />
                            </MenuItem>
                          ))}
                        </Select>
                        <br></br>
                      </FormControl>
                    </Grid> 



                    <Grid item xs={5} align="center">
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
       </Grid>
       </Grid>
       
       <Grid container direction="row" justify="center" alignItems="center" spacing={2}>


            <Grid item  xs={5} align="center">
            <Bar
            data={graphDataSize(distributorDataSliceLeft,yAxisHeightLeft,selectedMarkets)[0]}
            width={null}
            height={null}
            getDatasetAtEvent={(dataset) => handleChartClickLeft(dataset, 'targeted markets')}
            options={options}
          />
          </Grid>

          {/* LEGENDA IN THE MIDDLE */}
          <Grid item  xs={2} align="left">
                          <Grid item className={classes.gridBorder}  xs={12}>
                            <Grid item xs={12}>
                                  <Button style={MyTheme.palette.agarthaDarkBlue}></Button>
                                  &nbsp; Agartha - distributor
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.agarthaMiddleBlue}></Button>
                                  &nbsp; Agartha - both
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.agarthaLightBlue}></Button>
                                  &nbsp; Agartha - end user
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketDarkOrange}></Button>
                                  &nbsp; Cannazon - distributor
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketMiddleOrange}></Button>
                                  &nbsp; Cannazon - both
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketLightOrange}></Button>
                                  &nbsp; Cannazon - end user 
                                  </Grid>
                                  <br></br>
                                  
                                  
  
                                  </Grid>
                            </Grid>

  
          <Grid item  xs={5} align="center">
            <Bar
            data={graphDataSize(distributorDataSliceRight,yAxisHeightRight,selectedMarkets)[0]}
            width={null}
            height={null}
            getDatasetAtEvent={(dataset) => handleChartClickRight(dataset, 'targeted markets')}
            options={options}
          />
          </Grid>
          </Grid>

          <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>

    
          <Grid item xs={6} align="center">
            
          {/* LIST OF VENDORS UNDER THE LEFT CHART */}
          {renderListTargetedLeft? 
              <Grid item xs={12}>
                <br></br>
                      <Typography variant="subtitle2" className={classes.title} align="center">
                          All vendors {barchartClickMarketLeft} {barchartClickTypeLeft}
                      </Typography>
                      
              <List style={{width: "400px", height:"100px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
              {renderListTargetedLeft.map((vendor) => (
                   <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                        <ListItem   button>
                        <PersonIcon />
                        <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                        </ListItem>
                        </Link>
                        ))}
    
              </List>
              </Grid>
                             
                         :             <Grid item xs={12} align="center">
                         
                               <Typography variant="subtitle2" className={classes.title} align="center">
                                  No vendors selected
                               </Typography>
                       
                       <List style={{width: "400px",height:"100px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
                        <ListItem button>
                          <ListItemText style={{width: "150px"}} align="center">-</ListItemText>
                        </ListItem>
                    
         
                       </List>
                       </Grid>}
                       

                       </Grid>


                       <Grid item xs={6} align="center">
            
          {/* LIST OF VENDORS UNDER THE RIGHT GRAPH */}
            {renderListTargetedRight? 
                <Grid item xs={12} align="center">
                  <br></br>
                        <Typography variant="subtitle2" className={classes.title} align="center">
                            All vendors {barchartClickMarketRight} {barchartClickTypeRight}
                        </Typography>
                       
                <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
                {renderListTargetedRight.map((vendor) => (
                     <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                          <ListItem button>
                          <PersonIcon />
                          <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                          </ListItem>
                          </Link>
                          ))}
      
                </List>
                </Grid>
                               
                           :             <Grid item xs={12} align="center">
                           
                                 <Typography variant="subtitle2" className={classes.title} align="center">
                                    No vendors selected
                                 </Typography>
                                 <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
                          <ListItem button>
                            <ListItemText style={{width: "150px"}} align="center">-</ListItemText>
                          </ListItem>
                      
           
                         </List>
                         </Grid>}


                          
                            </Grid>


                            </Grid>


                            </div>


                      : <div></div>}



                     
        
            
{/* //////////////////////////////////////////////////////////////////////////////////////////////////////////////////             */}
             {/* DEFINE TARGETED MARKETS LAYOUT, IMPORTED FROM NETWORK SCRIPT CONSIDERING ITS SIZE */}
             {showResultsTargetedMarkets? 
             <Network ></Network> : <div></div>}
{/* //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// */}
             {/* DEFINE GROUP/INDIVIDUAL PAGE */}
             {showResultsCollaboration ? 
             <div>
              <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
              <Grid item xs={5} align="center">
   
           
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
       </Grid>
               


       <Grid item  xs={2} align="center">
                    
                      <FormControl className={classes.formControl}>
                        <InputLabel id="demo-mutiple-checkbox-label">Markets</InputLabel>
                        <Select
                          labelId="demo-mutiple-checkbox-label"
                          id="demo-mutiple-checkbox"
                          multiple
                          value={selectedMarkets}
                          onChange={handleChange}
                          input={<Input />}
                          renderValue={(selected) => selected.join(', ')}
                          MenuProps={MenuProps}
                        >
                          {uniqueMarkets.map((name) => (
                            <MenuItem key={name} value={name}>
                              <Checkbox checked={selectedMarkets.indexOf(name) > -1} />
                              <ListItemText primary={name} />
                            </MenuItem>
                          ))}
                        </Select>
                        <br></br>
                      </FormControl>
                    </Grid> 



                    <Grid item xs={5} align="center">
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
       </Grid>

       </Grid>


      <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
            <Grid item  xs={5}>
            <Bar
            data={graphDataSize(individualDataSliceLeft,yAxisHeightLeft,selectedMarkets)[0]}
            width={null}
            height={null}
            getDatasetAtEvent={(dataset) => handleChartClickLeft(dataset, 'collaboration')}
            options={options}
          />
          </Grid>
          {/* THE LEGENDA IN THE MIDDLE OF THE PAGE */}
          <Grid item xs={2} align="left">
         <Grid item className={classes.gridBorder}  xs={12}>
                            <Grid item xs={12}>
                            <Button style={MyTheme.palette.agarthaDarkBlue}></Button>
                                  &nbsp; Agartha - group
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.agarthaMiddleBlue}></Button>
                                  &nbsp; Agartha - individual
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.agarthaLightBlue}></Button>
                                  &nbsp; Agartha - unknown
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketDarkOrange}></Button>
                                  &nbsp; Cannazon - group
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketMiddleOrange}></Button>
                                  &nbsp; Cannazon - individual
                                  </Grid>
                                  <br></br>
                                  <Grid item xs={12}>
                                  <Button style={MyTheme.palette.darkmarketLightOrange}></Button>
                                  &nbsp; Cannazon - unknown  
                                  </Grid>
                                  <br></br>
                                  {/* <Button>
                                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:50}} onClick={handleClickOpenGroup} />
                                  </Button> */}
                                    
                                  </Grid>
                            </Grid>

                            <Grid item  xs={5} align="center">
            <Bar
            data={graphDataSize(individualDataSliceRight,yAxisHeightRight,selectedMarkets)[0]}
            width={null}
            height={null}
            getDatasetAtEvent={(dataset) => handleChartClickRight(dataset, 'collaboration')}
            options={options}
          />
          </Grid>
          </Grid>
    
    <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
          <Grid item xs={6} align="center">
            
          <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>
            {/* LIST OF VENDORS UNDER THE LEFT CHART */}
          {renderListCollaborationLeft? 
              <Grid item xs={4}>
                <br></br>
                      <Typography variant="subtitle2" className={classes.title} align="center">
                          All vendors {barchartClickMarketLeft} {barchartClickTypeLeft}
                      </Typography>
                      <br></br>
              <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
              {renderListCollaborationLeft.map((vendor) => (
                   <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                        <ListItem   button>
                        <PersonIcon />
                        <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                        </ListItem>
                        </Link>
                        ))}
    
              </List>
              </Grid>
                             
                         :             <Grid item xs={6} align="center">
                         <br></br>
                               <Typography variant="subtitle2" className={classes.title} align="center">
                                  No vendors selected
                               </Typography>
                       <List style={{width: "400px", overflow: 'auto'}}>

         
                       </List>
                       </Grid>}
                       </Grid>
          
    
                         </Grid>

                         <Grid item xs={6} align="center">
            
            <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>
              {/* LIST OF VENDORS UNDER THE RIGHT CHART */}
            {renderListCollaborationRight? 
                <Grid item xs={4}>
                  <br></br>
                        <Typography variant="subtitle2" className={classes.title} align="center">
                            All vendors {barchartClickMarketRight} {barchartClickTypeRight}
                        </Typography>
                        <br></br>
                <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
                {renderListCollaborationRight.map((vendor) => (
                     <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                          <ListItem button>
                          <PersonIcon />
                          <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                          </ListItem>
                          </Link>
                          ))}
      
                </List>
                </Grid>
                               
                           :             <Grid item xs={6} align="center">
                           <br></br>
                                 <Typography variant="subtitle2" className={classes.title} align="center">
                                    No vendors selected
                                 </Typography>
                         <List style={{width: "400px", overflow: 'auto'}}>
  
           
                         </List>
                         </Grid>}
                         </Grid>
            
      
                           </Grid>
                     
                            </Grid>



                          </div>
              
              : <div></div>}
  
{/* //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// */}
                        
          {/* DEFINE SPECIALIST/GENERALIST LAYOUT */}    
                  {showResultsSpecialist ? 
                  <div>
             <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
             <Grid item xs={5} align="center">
  
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
      </Grid>

      <Grid item  xs={2} align="center">
                    
                      <FormControl className={classes.formControl}>
                        <InputLabel id="demo-mutiple-checkbox-label">Markets</InputLabel>
                        <Select
                          labelId="demo-mutiple-checkbox-label"
                          id="demo-mutiple-checkbox"
                          multiple
                          value={selectedMarkets}
                          onChange={handleChange}
                          input={<Input />}
                          renderValue={(selected) => selected.join(', ')}
                          MenuProps={MenuProps}
                        >
                          {uniqueMarkets.map((name) => (
                            <MenuItem key={name} value={name}>
                              <Checkbox checked={selectedMarkets.indexOf(name) > -1} />
                              <ListItemText primary={name} />
                            </MenuItem>
                          ))}
                        </Select>
                        <br></br>
                      </FormControl>
                    </Grid> 


                   <Grid item xs={5} align="center">
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
      </Grid>
      </Grid>

      <Grid container direction="row" justify="center" alignItems="center" spacing={2}>

           <Grid item  xs={5} align="center">
           <Bar
           data={graphDataSize(specialistGeneralistDataSliceLeft,yAxisHeightLeft,selectedMarkets)[0]}
           width={null}
           height={null}
           getDatasetAtEvent={(dataset) => handleChartClickLeft(dataset, 'specialistGeneralist')}
           options={options}
         />
         </Grid>
        {/* LEGENDA IN THE MIDDLE OF THE PAGE */}
        <Grid item xs={2} align="left">
               <Grid item className={classes.gridBorder}  xs={12}>
                           <Grid item xs={12}>
                           <Button style={MyTheme.palette.agarthaDarkBlue}></Button>
                                 &nbsp; Agartha - specialist
                                 </Grid>
                                 <br></br>
                                 <Grid item xs={12}>
                                 <Button style={MyTheme.palette.agarthaLightBlue}></Button>
                                 &nbsp; Agartha - generalist
                                 </Grid>
                                 <br></br>
                                 <Grid item xs={12}>
                                 <Button style={MyTheme.palette.darkmarketDarkOrange}></Button>
                                 &nbsp; Cannazon - specialist
                                 </Grid>
                                 <br></br>
                                 <Grid item xs={12}>
                                 <Button style={MyTheme.palette.darkmarketLightOrange}></Button>
                                 &nbsp; Cannazon - generalist  
                                 </Grid>
                                 <br></br>
                                 {/* <Button>
                                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:50}} onClick={handleClickOpenSpecialist} />
                                  </Button> */}
                                   
                                 </Grid>
                           </Grid>

            <Grid item  xs={5} align="center">
           <Bar
           data={graphDataSize(specialistGeneralistDataSliceRight,yAxisHeightRight,selectedMarkets)[0]}
           width={null}
           height={null}
           getDatasetAtEvent={(dataset) => handleChartClickRight(dataset, 'specialistGeneralist')}
           options={options}
         />
         </Grid>
         </Grid>
         <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
         <Grid item xs={6} align="center">
           
         <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>
           {/* LIST OF VENDORS UNDER THE LEFT CHART */}
         {renderListSpecialistLeft ? 
             <Grid item xs={4}>
               <br></br>
                     <Typography variant="subtitle2" className={classes.title} align="center">
                         All vendors {barchartClickMarketLeft} {barchartClickTypeLeft}
                     </Typography>
                     <br></br>
             <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
             {renderListSpecialistLeft.map((vendor) => (
                  <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                       <ListItem   button>
                       <PersonIcon />
                       <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                       </ListItem>
                       </Link>
                       ))}
   
             </List>
             </Grid>
                            
                        :             <Grid item xs={6} align="center">
                        <br></br>
                              <Typography variant="subtitle2" className={classes.title} align="center">
                                 No vendors selected
                              </Typography>
                      <List style={{width: "400px", overflow: 'auto'}}>

        
                      </List>
                      </Grid>}
                      </Grid>
         
   
                        </Grid>


         <Grid item xs={6} align="center">
           
           <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>
             {/* LIST OF VENDORS UNDER THE RIGHT CHART */}
           {renderListSpecialistRight? 
               <Grid item xs={4}>
                 <br></br>
                       <Typography variant="subtitle2" className={classes.title} align="center">
                           All vendors {barchartClickMarketRight} {barchartClickTypeRight}
                       </Typography>
                       <br></br>
               <List style={{width: "400px", display:'flex', flexDirection:'row',overflow: 'auto' }}>
               {renderListSpecialistRight.map((vendor) => (
                    <Link to={{pathname: '/operational',state: [vendorOperationalTab]}} style={{ textDecoration: 'none' }}>
                         <ListItem button>
                         <PersonIcon />   
                         <ListItemText style={{width: "150px"}} align="center" onClick={(event) => handleVendorClick(vendor)}>{vendor}</ListItemText>
                         </ListItem>
                         </Link>
                         ))}
     
               </List>
               </Grid>
                              
                          :             <Grid item xs={6} align="center">
                          <br></br>
                                <Typography variant="subtitle2" className={classes.title} align="center">
                                   No vendors selected
                                </Typography>
                        <List style={{width: "400px", overflow: 'auto'}}>
  
          
                        </List>
                        </Grid>}
                        </Grid>
           
     
                          </Grid>
                           



                         
                           </Grid>


                           </div>
                      : <div></div> }          
            
  {/* ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////           */}
{/* DEFINE SHIPPING TO LAYOUT */}
     {showResultsShipping ?  
     <div>
     <Grid container direction="row" justify="center" alignItems="center" spacing={2}>
     <Grid item xs={5} align="center">

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
</Grid>

<Grid item  xs={2} align="center">
                   
             <FormControl className={classes.formControl}>
               <InputLabel id="demo-mutiple-checkbox-label">Markets</InputLabel>
               <Select
                  native
                 value={selectedCountryMarkets}
                 onChange={handleChange}
                 inputProps={{
                  name: 'age',
                  id: 'age-native-simple',
                }}> {countryMarkets.map((market) => (
                  <option value={market}>{market}</option>
                )

                )}
               </Select>
               
             </FormControl>
           </Grid> 


           <Grid item xs={5} align="center">
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
</Grid>
</Grid>
      <Grid container direction="row" justify="center" alignItems="center"   spacing={2}>
  <Grid item xs={5} align="center">
          <Line 
            data={processCountryData(countryDataMarketsSliceLeft, countryYAxisLeft)[0]}
          
            options = {{
              title: {
                display: true,
                text: `Distribution for all vendors that at least ship from ${countryNameLeft}`,
              

        },
              scales: {
                yAxes: [{
                  ticks:{               
                  suggestedMax: Math.max.apply(Math, [ processCountryData(countryDataMarketsSliceLeft, countryYAxisLeft)[1],  processCountryData(countryDataMarketsSliceRight, countryYAxisRight)[1]])

                  },
                  stacked: true,
                  scaleLabel: {
                    display: true,
                    labelString: 'Number of weeks'
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

            <Grid item  xs={2} align="center">
                          <Grid item className={classes.gridBorder}  xs={12}>
                            
                                  <br></br>
                                  {/* <Button>
                                  <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:50}} onClick={handleClickOpenShipping} />
                                  </Button> */}
                                     
  
                                  </Grid>
                            </Grid>

            <Grid item xs={5} align="center">
          <Line 
            data={processCountryData(countryDataMarketsSliceRight,countryYAxisRight)[0]}
         
            options = {{
              title: {
                display: true,
                text: `Distribution for all vendors that at least ship from ${countryNameRight}`,
              

        },
              scales: {
                yAxes: [{
                  ticks:{               
                  suggestedMax: Math.max.apply(Math, [ processCountryData(countryDataMarketsSliceLeft, countryYAxisLeft)[1],  processCountryData(countryDataMarketsSliceRight, countryYAxisRight)[1]])

                  },
                  stacked: true,
                  scaleLabel: {
                    display: true,
                    labelString: 'Sales in €'
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
            </div>
           : <div></div>} 
            
              <Tour
                    steps={steps}
                    isOpen={tourOpen}
                    onRequestClose={() => setTourOpen(false)}
                    startAt={16}
                    rounded={10}
                     />

           
        
    
      </div>)

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

export default MO;


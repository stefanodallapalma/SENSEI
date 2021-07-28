

import React, { Component,useEffect, useState,useCallback,useRef } from 'react';
import { withStyles,makeStyles } from '@material-ui/core/styles';import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import CloseIcon from '@material-ui/icons/Close';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import { useLocation,useHistory } from 'react-router-dom';
import PopoversideOperational from '../atoms/PopoversideOperational'
import { TextField } from '@material-ui/core'
import Video from '../operational.mp4'
import VideoPlayer from 'react-video-js-player'
import OndemandVideoIcon from '@material-ui/icons/OndemandVideo';
import Comments from "./Comments";
import commentBox from 'commentbox.io';
import MessageIcon from '@material-ui/icons/Message';
import PersonIcon from '@material-ui/icons/Person';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import Tour from 'reactour'
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import ArrowUpwardIcon from '@material-ui/icons/ArrowUpward';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';


// Set design configurations
const useStyles = makeStyles((theme) => ({
    formControl: {
      margin: theme.spacing(1),
      minWidth: 140,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },
    root: {
        minWidth: 275,
        maxWidth: 400,
      },
      appBar: {
        position: 'relative',
      },
      title: {
        marginLeft: theme.spacing(2),
        flex: 1,
      },
  }));

// Set theme for active tab (visible once the user has clicked on a vendor name)
  const theme = createMuiTheme({
      root: {
        maxWidth: 800
      },
    palette: {
      primary: {
        main: '#1092dd',
      },
      secondary: {
        main: '#FFFFF',
      }
    },
    notActiveTab:{
      fontSize:'13px',
      color:'white'
    },
    activeTab:{
      fontSize:'20px',
      fontWeight:'bold',
      color:'white'
    }
  });


  export default function Operational() {
    const location = useLocation();
    const history = useHistory();
   
    // This function is used to make sure that the tour functionality can be used
  // Once the page loads, it detects whether anything is present in the location.state
  // If that is the case, the tour is set to true
  // It will be called further on in the script
    function openTheTour(){
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
             It harnesses data, information and intelligence 
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
                The information sections have been divided by means of the 5 W's central to an investigation.
                Information is a combination of data that increases its value.
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
                  and marketplaces. 
                </Typography>
              },
              {
                content: <Typography variant="subtitle1">
                 Lastly, the dashboard also provides you with intelligence. Intelligence can be created by combining various
                 information sources, often done by analysts. Therefore, this dashboard allows you to store your relevant
                 insights and share these with others, learning from each other. 
                </Typography>
              },
              {
                selector:'.commentButton',
                content: <Typography variant="subtitle1">
                  When clicking on this icon, a comment section appears. Once you have logged in, you can comment, reply
                  and like other comments.
                </Typography>
              },
              {
                selector:'.mindmap',
                content: <Typography variant="subtitle1">
                 Additionally, clicking over here allows you to create a mindmap that only you can see, keeping track of
                 the insights you have obtained.
                </Typography>
              },
          
          ];

    var valueRef = useRef('')

    const videoSrc = Video;
  
    // Set useStates
    const classes = useStyles();
    const [openVideo, setOpenVideo] = useState(false);
    const [openComments, setOpenComments] = useState(false);
    const [data, setData] = useState([]);
    const [categoryData, setCategoryData] = useState([]);
    const [categories, setCategories] = useState([]);
    const [dataSlice, setDataSlice] = useState([]);
    const [activeVendorData,setActiveVendorData] = useState([]);
    const [activeVendorDataSlice, setActiveDataVendorSlice] = useState([]);
    const [dataNames,setDataNames] = useState([]);    
    const [timestamps, setTimestamps] = useState();
    const [timestamp, setTimestamp] = useState('');
    const [dates, setDates] = useState({});
    const [date, setDate] = useState({});
    const [countryData, setCountryData] = useState([]);
    const [country, setCountry] = useState('');
    const [sizeData, setSizeData] = useState('');
    const [size, setSize] = useState('');
    const [growingData, setGrowingData] = useState('');
    const [growing, setGrowing] = useState('');
    const [marketData, setMarketData] = useState('');
    const [market, setMarket] = useState('');
    const [showList, setShowList] = useState(false);
    const [activeVendor, setActiveVendor] = useState('');
    const [showInfoSection,setShowInfoSection] = useState(false);
    const [open, setOpen] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [loadedForChart, setLoadedForChart] = useState(false);
    const [valueTabs, setValueTabs] = React.useState(0);
    const [highlightedTab, setHighlightedTab] = useState([]);
    const [timestampsActiveVendor, setTimestampsActiveVendor] = useState([]);
    const [isTourOpen, setIsTourOpen] = useState(false);
    const [value, setValue] = useState(0);


    // Load data
    useEffect( async() => {
        const all_data = await axios.get('http://0.0.0.0:4000/operational');
        setData(all_data.data[0])
        setSizeData(["Large", "Medium","Small"]);
        setGrowingData(['Increased', 'Same/unknown', 'Decreased']);
        setCountryData(all_data.data[2]);
        setMarketData(all_data.data[3]);
        setTimestamps(all_data.data[4])
        const category_data = await axios.get('http://0.0.0.0:4000/productpage');
        setCategories(category_data.data[3])
        setCategoryData(category_data.data[4])
        
        setLoaded(true);
    }, [])
   
    // Load commentbox functionality
    useEffect( async() => {
        var comment = commentBox('5665558141861888-proj')
      })


      // Handle open/close comment section
      const handleClickOpenComments = () => {
        setOpenComments(true);
      };
      const handleCloseComments = (event) => {
        setOpenComments(false);
      };


  // Handle open/close video section
    const handleClickOpenVideo = () => {
        setOpenVideo(true);
      };
    const handleCloseVideo = (event) => {
        setOpenVideo(false); 
      };
    
    // Handle changes made to the filters
    const handleChangeCountry = (event) => {
      setCountry(event.target.value);
    };
    const handleChangeSize = (event) => {
        setSize(event.target.value);
      };
    const handleChangeGrowing = (event) => {
        setGrowing(event.target.value);
      };
    const handleChangeMarket = (event) => {
        setMarket(event.target.value);
      };
    const handleChangeTimestamp = (event) => {
        setTimestamp(event.target.value);
      };
    const handleClickOpen = () => {
        setOpen(true);
      };
    

    // Handles closing of the vendor screen
    const handleClose = (event) => {
        location.state = '';
        setOpen(false);
        setTimestampsActiveVendor([])
        setHighlightedTab([])
        setActiveVendorData([])
        setActiveVendor([])
        setValueTabs([]);
        setActiveDataVendorSlice([])
        setShowInfoSection(false);
        
        
        
      };

    // All the functionalities for the 'deselect all'
    const deleteAllFilters = () => {
            setCountry('');
            setSize('');
            setGrowing('');
            setMarket('');
            setTimestamp('');
            valueRef.current.value = ''
            setShowList(false)
            
        } 

        const allDataForVendor = (name) => {
            var requiredData = [];
            var timestampsForVendor = [];
            for (const record of data){
                if (record['name'] == name){
                    requiredData.push(record)
                    timestampsForVendor.push(record['timestamp'])
                }
            }
            setTimestampsActiveVendor(timestampsForVendor)
            setHighlightedTab(timestampsForVendor[0])
            setActiveVendorData(requiredData)
            setActiveDataVendorSlice(requiredData[0])
            return(requiredData)
        }
        





        // This function checks whether the dashboard has redirected the user from the treemap functionality
        // If the user has clicked on the 'investigate vendor' in the treemap window, he/she is supposed to 
        // immediately see all the info of this vendor. This is arranged within this functionality by
        // checking what the location.state[0] is.
    function runIt(){
        if (location.state !== undefined){
            if ( location.state[0] !== ''){
                
                for (const record of data){
                    if (record['name'] === location.state[0]){
        
                        allDataForVendor(record['name'])
                        setOpen(true)
                        
                        location.state = '';
                        return(null)
                    }
                }
                
            }
            
        }
            
        }
    
       // This function adds the right category to each vendor, thereby merging different inputs from the load function
       // This output is consequently used within the vendor windows.
        const addCategoryToVendors = (dataToAlter) => {
            var dataToReturn = []
            console.log(dataToAlter)

            for (const [vendor, timestamps] of Object.entries(categoryData)){
                for (const [timestamp, category] of Object.entries(timestamps)){
                    if (!(category.length == 0)){
                        for (let i=0; i < dataToAlter.length; i++){
                            if (dataToAlter[i]['timestamp'] == timestamp && dataToAlter[i]['name'] == vendor){
                                dataToAlter[i]['Drugs categories'] = category
                                dataToReturn.push(dataToAlter[i])
                    }
                    }
                } if (category.length == 0){
                    for (let i=0; i < dataToAlter.length; i++){
                        if (dataToAlter[i]['timestamp'] == timestamp && dataToAlter[i]['name'] == vendor){
                            dataToAlter[i]['Drugs categories'] = 'Not known, no products found for this vendor'
                            dataToReturn.push(dataToAlter[i])
                        }
                    }
                }

                    }
                }
            // All vendors for which no products are found are excluded up till this point. These are added here
            var allIncludedVendors = dataToReturn.map(record => record.name)
            .filter((value, index, categoryArray) => categoryArray.indexOf(value) === index);

            for (let i=0; i < dataToAlter.length; i++){
                if (!(dataToReturn.includes(dataToAlter[i]['name']))){
                    dataToReturn.push(dataToAlter[i])
                }
                
            }

            return(dataToReturn)
            }



    if (loaded){
      // Transform the timestamps to actual dates
      var actualDates = []
      for (let i = 0; i < timestamps.length; i++) {
        var actualDate  = new Date(timestamps[i] * 1000)
        actualDates.push(actualDate.getDate() + '-' + (actualDate.getMonth()+1) + '-' + actualDate.getFullYear())
      }
    setDates(actualDates)
    openTheTour()
    setData(addCategoryToVendors(data))
    setLoaded(false)
    setLoadedForChart(true)

    }


    

    if (loadedForChart){

      

         runIt();
         
        // This function filters out all the vendors that meet the filters that are set by the user
        // The output are all the vendor names that meet the requirements from the filter
        const DataToRender = () => {
            var outputTextfield = valueRef.current.value
            var finalDataNames = [];
            var finalData = [];

            if (outputTextfield === ''){
                for (const record of data){
                    if (record['timestamp'] === timestamp || timestamp === ''){
                        if (record['ships_from'].includes(country) || country === ''){
                            if (record['market'] === market || market === ''){
                                if (record['size'] === size || size === ''){
                                    if (record['percentual_change'] === growing || growing === ''){
                                        finalData.push(record)
                                        
                                        //finalData.push(record)
                                    }
                                }
                            }
                            
                        }
                        
                    }
                }
            } if (outputTextfield !== ''){
                for (const record of data){
                    if (record['name'].includes(outputTextfield)){
                        if (record['timestamp'] === timestamp || timestamp === ''){
                            if (record['ships_from'].includes(country)  || country === ''){
                                if (record['market'] === market || market === ''){
                                    if (record['size'] === size || size === ''){
                                        if (record['percentual_change'] === growing || growing === ''){
                                            finalData.push(record)
                                            
                                            
                                        
                                        }
                                    }
                                }
                                
                            }
                            
                        }
                    }
         
                    }
            }
            finalData.sort(function(first, second) {
                return second['Estimated sales since 2021 - week 1'] - first['Estimated sales since 2021 - week 1'];
               });
            
            // console.log(finalData)
            
            for (let i = 0; i < finalData.length; i++){
                if (!(finalDataNames.includes(finalData[i]['name']))){
                    finalDataNames.push(finalData[i]['name'])
                }
                
            }
            
            setDataNames(finalDataNames)
            console.log(finalDataNames)
            setDataSlice(finalData)
            return (null)
            
        }


        
        // Handles the timestamp change within the vendor windows
        const handleChangeTabs = (event, newValue) => {
            setValueTabs(newValue);
            setActiveDataVendorSlice(activeVendorData[newValue - 1])
            console.log(timestampsActiveVendor)
            console.log(timestampsActiveVendor[newValue-1])
            setHighlightedTab(timestampsActiveVendor[newValue-1])

          };
    

        


        return(
            <div className="hi">
            
                
                <Grid container spacing={0} direction="column" alignItems="center"  style={{ minHeight: '100vh' }}>
                    <br></br>
                <Grid item xs={11}>
                    Select your criteria and click 'Go' to get a list of vendors
                    </Grid>


                {/* ALL THE FILTERS */} 
                <Grid item xs={10}>
                    <div className="select">
                <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-select-label" >Collection date</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={timestamp}
                        
                        onChange={handleChangeTimestamp}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                        {timestamps.map((x) => (
                        <MenuItem value={x}>{x}</MenuItem>
                            )

                         )}
                        </Select>
                    </FormControl>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-select-label">Country of origin</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={country}
                        onChange={handleChangeCountry}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                        {countryData.map((x) => (
                        <MenuItem value={x}>{x}</MenuItem>
                            )

                         )}
                        </Select>
                    </FormControl>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-select-label">Market</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={market}
                        onChange={handleChangeMarket}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                        {marketData.map((x) => (
                        <MenuItem value={x}>{x}</MenuItem>
                            )

                         )}
                        </Select>
                    </FormControl>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-select-label">Size</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={size}
                        onChange={handleChangeSize}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                        {sizeData.map((x) => (
                        <MenuItem value={x}>{x}</MenuItem>
                            )

                         )}
                        </Select>
                    </FormControl>
                    <FormControl className={classes.formControl}>
                        <InputLabel id="demo-simple-select-label">Sales traction</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={growing}
                        onChange={handleChangeGrowing}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                        {growingData.map((x) => (
                        <MenuItem value={x}>{x}</MenuItem>
                            )

                         )}
                         </Select>
                    </FormControl>
                    </div>

                    {/* VIDEO SECTION */} 
                    <Button>
                            <OndemandVideoIcon style={{color:'#FF6700', fontSize:30}}  onClick={handleClickOpenVideo} ></OndemandVideoIcon>
                        </Button>
                        <Dialog
                        open={openVideo}
                        onClose={handleCloseVideo}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"md"}
                    >
                        <VideoPlayer src={Video} width="720" height="420"></VideoPlayer>
                        <Button onClick={handleClose} color="primary">
                        Close
                      </Button></Dialog>

                        <Button>
                        <MessageIcon style={{color:'#FF6700', fontSize:30}} onClick={handleClickOpenComments} ></MessageIcon>
                   </Button> 
                  {/* COMMENT SECTION */}       
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
                
                    <Grid item xs={10}>
                        <br></br>
                    <TextField
                            id='outlined-textarea'
                            label='Vendor name'
                            placeholder='Be aware of capital letters!'
                            variant='outlined'
                            inputRef={valueRef}   //connecting inputRef property of TextField to the valueRef
                            />
                    
                      </Grid>
                      <br></br>
                      <Button variant="outlined" size="small" color="primary" onClick={() => {deleteAllFilters()}} >
                      Deselect all</Button>
                        <PopoversideOperational/>
                        
                    <Grid className="go" item xs={3}>
                        <br></br>
                        <Button variant="contained" color="primary" onClick={() => {DataToRender(); setShowList(true)}}>Go - sorted by sales</Button>
                    </Grid>
                    
                {/* LIST OF VENDORS SECTION */} 
                    {showList ? 
                    <Grid item xs={6}>
                        <br></br>
                        <Typography variant="h6" className={classes.title} align="center">
                            {dataNames.length} vendors found
                        </Typography>
                    <List component="nav" aria-label="secondary mailbox folders">
                        {dataNames.map((vendor) => (
                        <ListItem button>
                        <PersonIcon />
                        <ListItemText  align="center" onClick={() => {allDataForVendor(vendor);setActiveVendor(vendor);handleClickOpen()}}>
                            {vendor}</ListItemText>
                        </ListItem>
                       
                        ))}
                    </List>
                    </Grid>
                    : <div></div>}


              {/* VENDOR WINDOW SECTION */} 
            <MuiThemeProvider theme={theme}>
                <Dialog  open={open} onClose={handleClose} maxWidth={"md"} >
                        <AppBar className={classes.appBar}>
                        <Tabs value={value} onChange={handleChangeTabs} aria-label="simple tabs example">
                        <Toolbar>
                            <IconButton edge="start" color="inherit" onClick={(event) => {event.preventDefault(); handleClose()}} aria-label="close">
                            <CloseIcon />
                            </IconButton>
                            <Typography variant="h6" className={classes.title}>
                            {activeVendor['name']}
                            </Typography>
                        </Toolbar>
                        {timestampsActiveVendor.map((vendorTimestamp) => (
                            <Tab  style={highlightedTab === vendorTimestamp ? theme.activeTab : theme.notActiveTab} label={vendorTimestamp}   ></Tab>
                        ))}
                        </Tabs>
                        </AppBar>
                        <List className={classes.root}>
                        <ListItem >
                            <ListItemText primary="Vendor" secondary={activeVendorDataSlice['name']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Market" secondary={activeVendorDataSlice['market']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Data collection date" secondary={activeVendorDataSlice['timestamp']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Drugs types sold" secondary={activeVendorDataSlice['Drugs categories']} />
                        </ListItem>

                        
                        <ListItem >
                            <ListItemText primary="Ships from" secondary={activeVendorDataSlice['ships_from']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Ships to" secondary={activeVendorDataSlice['ships_to']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Size" secondary={activeVendorDataSlice['size']} />
                        </ListItem>
                        {activeVendorDataSlice['percentual_change'] == 'Decreased' ? 
                        <ListItem >
                            <ListItemText primary="Sales traction" secondary={<ArrowDownwardIcon style={{color:'#FF0000'}} />} />
                        </ListItem>
                        : <ListItem >
                            <ListItemText primary="Sales traction" secondary={<ArrowUpwardIcon style={{color:'#00FF00'}} />} />
                            </ListItem>}
                        {/* <ListItem >
                            <ListItemText primary="Sales traction" secondary={activeVendorDataSlice['percentual_change']} />
                        </ListItem> */}
                        <ListItem >
                            <ListItemText primary="Estimated sales since 2021 - week 1 in euro's" secondary={'€'+ activeVendorDataSlice['Estimated sales since 2021 - week 1']} />
                        </ListItem>
    
                        <ListItem >
                            <ListItemText primary="Collaboration" secondary={activeVendorDataSlice['group_individual']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Email" secondary={activeVendorDataSlice['email']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Phone number" secondary={activeVendorDataSlice['phone number']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Other markets" secondary={activeVendorDataSlice['Other markets']} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Wickr username" secondary={activeVendorDataSlice['wickr']} />
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary="Info"  secondary="Open up the info from the vendor, ONLY WHEN AUTHORISED!" onClick={() =>setShowInfoSection(true)}/>
                            </ListItem>
            
                        {showInfoSection ? 
                                
                                <ListItemText className={classes.root} secondary={activeVendorDataSlice['info']} />
                                
                            :<div></div>}
                            
                        </List>
                        <ListItem >
                            <ListItemText primary="PGP" secondary={activeVendorDataSlice['pgp']} />
                        </ListItem>
                       
                        
                    </Dialog>
                    </MuiThemeProvider>   
                </Grid>
                <Tour
                    steps={steps}
                    isOpen={isTourOpen}
                    onRequestClose={() => setIsTourOpen(false)}
                    startAt={9}
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

}}



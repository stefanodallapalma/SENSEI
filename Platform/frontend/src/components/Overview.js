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
import Paper from '@material-ui/core/Paper';
import { GiConsoleController, GiMedicines } from "react-icons/gi";
import Button from '@material-ui/core/Button';
import { MdBusinessCenter } from "react-icons/md"
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import PersonIcon from '@material-ui/icons/Person';
import { IoLocationSharp } from "react-icons/io5";
import Box from '@material-ui/core/Box';
import { useLocation } from 'react-router-dom';
import Tour from 'reactour'
import { WorldMap } from "react-svg-worldmap"
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogActions from '@material-ui/core/DialogActions';
import Dialog from '@material-ui/core/Dialog';



const useStyles = makeStyles((theme) => ({
  buttons: {
    display: 'flex',
    justifyContent: "center",
    alignItems:"center"
  },
  paper: {
    borderRadius: 16,
    padding: 10

  }
}));




function Overview() {
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


    // Define all the useStates
    const classes = useStyles();
    const [openInfo, setOpenInfo] = useState(false);
    const [openHow, setOpenHow] = useState(false);
    const [openWho, setOpenWho] = useState(false);
    const [openWhere, setOpenWhere] = useState(false);
    const [openRaw, setOpenRaw] = useState(false);
    // useStates required for the 'what' section
    const [productData, setProductData] = useState([]);
    const [productDataSlice, setProductDataSlice] = useState([]);
    const [allCountries, setAllCountries] = useState([]);
    const [countryName, setCountryName] = useState('');
    const [allCategories, setAllCategories] = useState([]);
    const [allCategoriesTypeSlice,setAllCategoriesTypesSlice] = useState([]);
    const [loaded, setLoaded] = useState(false)
    const [open, setOpen] = useState(true);
    // useStates required for the 'how' section
    const [timestamps, setTimestamps] = useState([]);
    const [distributorData,setDistributorData] = useState([]);
    const [distributorDataSlice,setDistributorDataSlice] = useState([]);
    const [distributorEndUser, setDistributorEndUser] = useState('');
    const [specialistGeneralistData,setSpecialistGeneralistData] = useState([]);
    const [specialistGeneralistDataSlice,setSpecialistGeneralistDataSlice] = useState([]);
    const [specialistGeneralist, setSpecialistGeneralist] = useState('');
    const [individualData,setIndividualData] = useState([]);
    const [individualDataSlice,setIndividualDataSlice] = useState([]);
    const [individualType, setIndividualType] = useState('');
    // useStates for the 'who'  section
    const [vendorData, setVendorData] = useState('');
    const [largestVendor, setLargestVendor] = useState('');
    // useStates for the 'where' section
    const [graphData, setGraphData] = useState({});
    const [selectedGraphData, setSelectedGraphData] = useState([]);
    const [mapData, setMapData] = useState({});
    const [mapDataSlice, setMapDataSlice] = useState({});
    const [calculated, setCalculated] = useState(false);
    const [isTourOpen, setIsTourOpen] = useState(false);





    useEffect( async() => {
      // Load data for the 'what' section
      const results = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/productpage");
      setProductData(results.data[0]['All markets'])
      setProductDataSlice(results.data[0]['All markets']['United States'])
      setAllCountries(Object.keys(results.data[5]))
      setAllCategories(results.data[2])
      for (const [category, drugs] of Object.entries(results.data[4])){
        setAllCategoriesTypesSlice(drugs)
        break
      }
      setCountryName('United States')

      // load data for the 'how' section
      const all_data = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/product");
      setTimestamps(all_data.data[0])
      setDistributorData(all_data.data[1])
      setDistributorDataSlice(all_data.data[1]['United States'])

      const specialistData = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/productpage");
      setSpecialistGeneralistData(specialistData.data[5])
      setSpecialistGeneralistDataSlice(specialistData.data[5]['United States'])

      const individual_data = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/nlp");
      setIndividualData(individual_data.data[0])
      setIndividualDataSlice(individual_data.data[0]['United States'])

      const data_vendor = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/operational");
      setVendorData(data_vendor.data[0])
      
      // Load data for the 'where' section
      const results_reviews = await axios.get("http://" + process.env.REACT_APP_BACKEND_HOST + ":" + process.env.REACT_APP_BACKEND_PORT + "/reviews");
      setMapData(results_reviews.data[2])
      setMapDataSlice(results_reviews.data[2]["2021- week 4"])
      setLoaded(true)

    
      }, []);


      // This function transforms the input data to its correct format for the area chart in the 'what' section
      const productLineFunction = (dataToUse) => {
        var allData = []
        //var colours = ['rgb(47,75,124)','rgb(102,81,145)',"rgb(0,63,92)", 'rgb(160,81,149)', 'rgb(212,80,135)','rgb(249,93,106)', 'rgb(255,124,67)', 'rgb(255,166,0)' ]
        var colours = [ 'rgb(209, 99, 230)', 'rgb(184, 0, 88)', 'rgb(0, 140, 249)', 'rgb(0, 110, 0)', 'rgb(0, 187, 173)', 'rgb(235, 172, 35)', 'rgb(89, 84, 214)']
        //xgfs_normal12 = [(235, 172, 35), (184, 0, 88), (0, 140, 249), (0, 110, 0), (0, 187, 173), (209, 99, 230), (178, 69, 2), (255, 146, 135), (89, 84, 214), (0, 198, 248), (135, 133, 0), (0, 167, 108), (189, 189, 189)]
  
        var colourCounter = 0
  
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
    
        return ({
          labels: timestamp,
          datasets:allData
        })
      }
      





      // This function is used to define the biggest vendor for the country that the user has selected
      const calculateBiggestVendors = (nameOfCountry) => {
        var biggestVendor = []
        console.log("COUNTRY NAME")
        console.log(nameOfCountry)
        console.log("COUNTRY LIST")
        console.log(allCountries)

        for (let i = 0; i < vendorData.length; i++){
          console.log("VENDOR COUNTRY")
          console.log(vendorData[i]['ships_from'])
          if (vendorData[i]['ships_from'].includes(nameOfCountry) || (nameOfCountry === "All" && allCountries.includes(vendorData[i]['ships_from']))){
            if (biggestVendor.length === 0){
              biggestVendor.push(vendorData[i])  
            } else {
            if (vendorData[i]["Estimated sales since 2021 - week 1"] > biggestVendor[0]["Estimated sales since 2021 - week 1"]){
              biggestVendor = []
              biggestVendor.push(vendorData[i])
            }
          }
        }}
        console.log(vendorData)
        if (biggestVendor.length === 0) {
            console.log("Vendor not available")
            setLargestVendor("Vendor not available")
        } else {
            console.log(biggestVendor[0]['name'])
            setLargestVendor(biggestVendor[0]['name'])
        }

        return(null)
      }
      
      // This function makes sure all changes are made when the user selects a different country
      const handleChange = (event) => {
        setProductDataSlice(productData[event.target.value])
        setCountryName(event.target.value)
        setDistributorDataSlice(distributorData[event.target.value])
        setDistributorDataSlice(distributorData[event.target.value])
        setSpecialistGeneralistDataSlice(specialistGeneralistData[event.target.value])
        setIndividualDataSlice(individualData[event.target.value])
        doCalculations(distributorData[event.target.value], specialistGeneralistData[event.target.value],individualData[event.target.value] )
        calculateBiggestVendors(event.target.value)
        setSelectedGraphData(graphData[event.target.value]);
        

  
      }

      //Calculations for the 'how' section
      const doCalculations = (dataToUseDistributor, dataToUseSpecialist, dataToUseIndividual) => {
        var lastTimestamp = timestamps[timestamps.length - 1]
        // Do the calculations for Distributor- End user 
        var endUser = 0
        var distributor = 0
        var both = 0
        for (const [type, times] of Object.entries(dataToUseDistributor)){
          for (const [time, vendors] of Object.entries(times)){
            console.log(time)
            if (time === lastTimestamp){
              for (const [market, vendor] of Object.entries(vendors)){
                 if (type === 'Distributor'){
                    distributor += vendor.length
                 }
                 if (type === 'End user'){
                    endUser += vendor.length
                 }
                 if (type === 'Both'){
                    both += vendor.length
                 }
            }
          }
        }
      }
      console.log(endUser, distributor, both)
      // Take max value of the 3 categories
      if (endUser > distributor && endUser > both){
        setDistributorEndUser('selling to end consumers')
      }
      if (both > distributor && both > endUser){
        setDistributorEndUser('both selling to end consumers and serve as point of distribution, selling to other vendors')
      }
      if (distributor > endUser && distributor > both){
        setDistributorEndUser('a point of distribution, selling to other vendors')
      }
      if (distributor === endUser && distributor > 0){
        setDistributorEndUser('both selling to end consumers and serve as point of distribution, selling to other vendors')
      }
      if (distributor === both && distributor > 0){
        setDistributorEndUser('both selling to end consumers and serve as point of distribution, selling to other vendors')
      }
      if (endUser === both && endUser > 0){
        setDistributorEndUser('both selling to end consumers and serve as point of distribution, selling to other vendors')
      }
      if (endUser === 0 && both === 0 && distributor === 0){
        setDistributorEndUser('no product or reviews are found for this country at the last moment of data collection')
      }
      console.log(distributorEndUser)
      
      // Do calculations for Specialist - generalist
      var specialist = 0
      var generalist = 0
      for (const [type, times] of Object.entries(dataToUseSpecialist)){
        for (const [time, vendors] of Object.entries(times)){
          if (time === lastTimestamp){
            for (const [market, vendor] of Object.entries(vendors)){
               if (type === 'Specialist'){
                specialist += vendor.length
               }
               if (type === 'Generalist'){
                generalist += vendor.length
               }
          }
        }
      }
    }
    console.log(specialist, generalist)
    if (specialist > generalist){
      setSpecialistGeneralist('specialized in one product category')
    }
    if (specialist < generalist){
      setSpecialistGeneralist('offering products from a variety of categories')
    }
    if (specialist === generalist){
      setSpecialistGeneralist('both specialists and generalists')
    }
    if (specialist === 0 && generalist === 0){
      setSpecialistGeneralist('unknown whether vendors are specialists or generalists')
    }

    //Do calculations for Group - individual
    var individual = 0
    var group = 0
    for (const [type, times] of Object.entries(dataToUseIndividual)){
      for (const [time, vendors] of Object.entries(times)){
        if (time === lastTimestamp){
          for (const [market, vendor] of Object.entries(vendors)){
             if (type === 'Group'){
              group += vendor.length
             }
             if (type === 'Individual'){
              individual += vendor.length
             }

        }
      }
    }
  }
  console.log(individual, group)
    if (individual > group){
      setIndividualType('operating alone')
    }
    if (individual < group){
      setIndividualType('operating in a group')
    }
    if (individual === group){
      setIndividualType('equally often operating in a group as alone')
    }
    if (individual === 0 && group === 0){
      setIndividualType('unknown whether vendors are operating in a group or alone')
    }
      
      return(null)
    }
  

    // These functions handle opening or closening the information sections by the user
    const handleCloseInfo = (event) => {
      setOpenInfo(false);
    };
    const handleOpenInfo = () => {
      setOpenInfo(true);
    };
    const handleCloseWho = (event) => {
      setOpenWho(false);
    };
    const handleOpenWho = () => {
      setOpenWho(true);
    };
    const handleCloseHow = (event) => {
      setOpenHow(false);
    };
    const handleOpenHow = () => {
      setOpenHow(true);
    };
    const handleCloseWhere = (event) => {
      setOpenWhere(false);
    };
    const handleOpenWhere = () => {
      setOpenWhere(true);
    };
    const handleCloseRaw = (event) => {
      setOpenRaw(false);
    };
    const handleOpenRaw = () => {
      setOpenRaw(true);
    };


     
        
    
      if (loaded){
        runIt()
        doCalculations(distributorDataSlice, specialistGeneralistDataSlice, individualDataSlice)
        setLargestVendor(calculateBiggestVendors(countryName))
        console.log(calculateBiggestVendors(countryName))
        setLoaded(false)
        setCalculated(true)


        
      }

      if (calculated){
  
    return(
        <div className="overview">
          <Grid container direction="row" justify="center" aligItems="center">
           <Grid item xs={12} align="center">
           <br></br>
           <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-simple">Country</InputLabel>
                <Select
                  native
                  value={countryName}
                  onChange={handleChange}
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
       <br></br>
       <br></br>
           </Grid>
           <Grid container direction="row" justify="space-around" aligItems="center">
             <Grid item xs={4} align="center">
           <Grid container direction="column" justify="space-around" aligItems="center">
             <Grid item xs={12} align="center">
              <Paper className={classes.paper}>
              <GiMedicines size={25} />
              <Typography variant="h6">
                What?
              </Typography>
              <Button>
              <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:20}} onClick={handleOpenInfo} />
              </Button>
              {/* INFORMATION SECTION 'WHAT' */} 
              <Dialog
                        open={openInfo}
                        onClose={handleCloseInfo}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                        fullWidth = {true}
                    > 
                    <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                      What?
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
              <br></br>
              {/* 'WHAT' GRAPH */} 
              <Line 
                    data={productLineFunction(productDataSlice)}
                      
                    options = {{
                      responsive:true,
                      scales: {
                        yAxes: [{
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
                 <Button variant="contained" color="primary" size="small" onClick={() => {history.push({pathname: '/product' })}}>
                   Go to page</Button>
              </Paper>
              
             </Grid>
             <Grid item xs={12} align="center">
             <br></br>
           
           
           {/* WHO SECTION */} 
             <Paper className={classes.paper}>
             <PersonIcon size={15} />
              <Typography variant="h6">
                Who?
              </Typography>
              <Button>
              <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:20}} onClick={handleOpenWho}/>
              </Button>
              <Dialog
                    open={openWho}
                    onClose={handleCloseWho}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                    fullWidth = {true}
                > 
                <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                  Who?
                </DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    Allows you to identify interesting vendors based on the filtering you apply. 
                    Personal data is left out and aliases are pseudonimized since prior authorisations is required
                    if you want to structurally collect data on a data subject.
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <Button autoFocus onClick={handleCloseWho} color="primary">
                    Close
                  </Button>
                </DialogActions>
  
                </Dialog>     
              <Typography variant="subtitle1">
              Based on your selected criteria, allows you to explore data on vendors.
              </Typography>
              <Typography variant="subtitle1">
                Based on the sales, this is the largest vendor for your country:
              </Typography>
              <List component="nav">
              <ListItem >
                  
                  <ListItemText  align="center" >
                  <PersonIcon /> &nbsp;&nbsp;
                    {largestVendor}</ListItemText>
                  </ListItem>
                  </List>
              <Button variant="contained" color="primary" size="small" onClick={() => {history.push({pathname: '/operational'})}}>
              Go to page</Button>
             </Paper>
             </Grid>
             </Grid>
             </Grid>
             <Grid item xs={3} align="center">
                    <Grid item xs={12}>
                    
            {/* RAW DATA SECTION */} 
             <Paper className={classes.paper}>
             <IoLocationSharp size={15} />
              <Typography variant="h6">
                Raw data
              </Typography>
              <Button>
              <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:20}} onClick={handleOpenRaw}/>
              </Button>
              <Dialog
                    open={openRaw}
                    onClose={handleCloseRaw}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                    fullWidth = {true}
                > 
                <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                  Raw data
                </DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    Allows you to take a closer look at the raw data, giving you the ability to search and sort.
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <Button autoFocus onClick={handleCloseRaw} color="primary">
                    Close
                  </Button>
                </DialogActions>
  
                </Dialog>     
              <Typography variant="subtitle1">
              Allows you to explore the raw data
              </Typography>
              <Typography variant="subtitle1">
              For the selected country, the following data has been found:
              </Typography>
              <ul>
                  <li>7 vendors</li>
                  <li>84 products</li>
                  <li>2560 reviews</li>
                  <li>sell on multiple marketplaces</li>
                  
                </ul>
        
              <Button variant="contained" color="primary" size="small" onClick={() => {history.push({pathname: '/vendortable'})}}>
                Go to page</Button>
             </Paper>
                    </Grid>
             </Grid>


        {/* HOW SECTION */} 
             <Grid item xs={4} align="center">
           <Grid container direction="column" justify="space-around" aligItems="center">
           <Grid item xs={12} align="center">
             <Paper className={classes.paper}>
             < MdBusinessCenter size={15} />
              <Typography variant="h6">
                How?
              </Typography>
              <Button>
              <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:20}} onClick={handleOpenHow}/>
              </Button>
              <Dialog
                    open={openHow}
                    onClose={handleCloseHow}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                    fullWidth = {true}
                > 
                <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                  How?
                </DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    This page tells you more about the way vendors operate on the darkweb by analysing their business plan.
                    It does so for all the vendors found. If you want to discover how a single vendor evolves over time, 
                    you can find his/her information on the "Who" page, allowing you to browse through the 
                    available information. 
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <Button autoFocus onClick={handleCloseHow} color="primary">
                    Close
                  </Button>
                </DialogActions>
  
                </Dialog>     
              <Typography variant="subtitle1">
              Tells you about the bussines plan of vendors on the darkweb.
              </Typography>
              <Typography variant="subtitle1">
                For the last moment of data collection, most vendors from this country are:
                <ul>
                  <li>{distributorEndUser}</li>
                  <li>{specialistGeneralist}</li>
                  <li>{individualType}</li>
                  <li>sell on multiple marketplaces</li>
                  
                </ul>
              </Typography>
              <Button variant="contained" color="primary" size="small" onClick={() => {history.push({pathname: '/mo'})}}>
                Go to page</Button>
             </Paper>
              </Grid>
           
             {/* WHERE SECTION */} 
             <Grid item xs={12} align="center">
           <br></br>
             <Paper className={classes.paper}>
             <IoLocationSharp size={15} />
              <Typography variant="h6">
                Where?
              </Typography>
              <Button>
              <InfoOutlinedIcon  style={{color:'#1092dd', fontSize:20}} onClick={handleOpenWhere}/>
              </Button>
              <Dialog
                    open={openWhere}
                    onClose={handleCloseWhere}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"  maxWidth={"sm"}
                    fullWidth = {true}
                > 
                <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">
                  Where?
                </DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    This page tells you more about the sales development over time on marketplace, country 
                    and vendor level. Please carefully read the information sections on this page to 
                    know how these calculations have been done. 
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <Button autoFocus onClick={handleCloseWhere} color="primary">
                    Close
                  </Button>
                </DialogActions>
  
                </Dialog>   
              <Typography variant="subtitle1">
              Tells you about the estimated sales on marketplace, country and vendor level.
              </Typography>
              
              <br></br>
              
                          
                          <WorldMap color="#FF0000"  value-suffix="people" size='md' data={mapDataSlice} />
                          
        
              <Button variant="contained" color="primary" size="small" onClick={() => {history.push({pathname: '/treemap'})}}>
                Go to page</Button>
             </Paper>
              </Grid>
           </Grid>
           </Grid>
           </Grid>
           </Grid>
           <Tour
                    steps={steps}
                    isOpen={isTourOpen}
                    onRequestClose={() => setIsTourOpen(false)}
                    startAt={1}
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

export default Overview
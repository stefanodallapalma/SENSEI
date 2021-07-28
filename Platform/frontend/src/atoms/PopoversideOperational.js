// This script creates the information section for the 'who' page
// Import necessary packages and scripts
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Popper from '@material-ui/core/Popper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
import { IconButton } from '@material-ui/core';
import Fade from '@material-ui/core/Fade';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
  typography: {
    padding: theme.spacing(2),
  },
}));

// Create export function
export default function SimplePopover(props) {

    // Define the useStates
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [open, setOpen] = React.useState(false);
    const [placement, setPlacement] = React.useState();
    const classes = useStyles();
  
    const handleClick = (newPlacement) => (event) => {
      setAnchorEl(event.currentTarget);
      setOpen((prev) => placement !== newPlacement || !prev);
      setPlacement(newPlacement);
    };

  

  return (
    <div>
        <IconButton  variant="contained" color="primary" onClick={handleClick('right-start')} >
              <HelpOutlineIcon />
              </IconButton>
              <Popper open={open} anchorEl={anchorEl} placement={placement} transition>
        {({ TransitionProps }) => (
          <Fade {...TransitionProps} timeout={600}>
            <Paper>
              <Typography className="sidepopoverOperational">
                  <b>Size</b>
                  <br></br>
                  The size of a vendor is determined by the amount of reviews. All vendors are assigned to a specific group
                  based on the quartile they belong to. Hence, the assigned size is relative to the other vendors in the
                  dataset. If the amount of reviews a vendor receives fall within the highest 25% group, the vendor is large.
                  If the amount of sales fall within the lowest 25% group, the vendor is small. A review amount in between
                  means the vendor is of medium size.
                  <br></br>
                  <br></br>
                  <b>Sales traction</b>
                  <br></br>
                  This refers to whether the vendor has increased/decreased the sales since the start of 2020, based on the amount of reviews 
                  he/she has received. The average monthly amount of reviews are computed for the first 6 months and 
                  this is compared to the average monthly amount of reviews up untill the last moment of data collection.
                  The percentual difference is calculated between these 2 averages to determine whether the vendor
                  has increased/decreased the amount of sales. If a vendor has very little sales in one of these 2 time periods
                  the change in the amount of reviews cannot be calculated, therefore the category same/unknown is included.
                    
                   
              </Typography>
            </Paper>
          </Fade>
        )}
      </Popper>
            
      
    </div>
  );
}
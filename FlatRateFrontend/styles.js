import { Dimensions, Platform, StyleSheet } from "react-native";
import colors from "./colors.js";
import fonts from "./fonts.js"

const {width : screenWidth} = Dimensions.get('window');

export default StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#ffa700',
      alignItems: 'center',
      justifyContent: 'center'
    },

    engageBgContainer: {
      flex: 1,
      backgroundColor: '#C8ABED',
      alignItems: 'center',
      justifyContent: 'space-evenly'
    },

    buttonContainer: {
      flex: 1,
      backgroundColor: '#EDCCAB',
      alignItems: 'center',
      justifyContent: 'center',
    },

    inputContainer: {
      flex: 0,
      backgroundColor: '#d9d9d9',
      alignItems: 'center',
      justifyContent: 'center',
      height : 60,
      width: 300,
      borderColor: colors.purple,
      borderWidth: 2,
      borderBottomWidth: 4,
      borderRightWidth: 4,
      paddingLeft: 20,
      paddingBottom: 4,
      fontSize: 24, // need to also make font grey at first,
      color: colors.purple,
      borderRadius: 10,
      fontFamily: fonts.prompt,
      marginBottom: 10
    },

    button: {
      color: '#e17511',
      flex: 1,
    },

    text: {
      color:'white',
      fontFamily: fonts.prompt,
      fontSize: 40,
      textAlign: 'center'
    },

    walkthroughText : {
      color: 'black',
      fontFamily : fonts.prompt,
      fontSize : 22,
      textAlign: 'center'
    },

    purpleText: {
      color:'#2e2848',
      fontFamily: fonts.prompt,
      fontSize: 40,
      textAlign: 'center'
    },
  
    formText: {
      color:'blue',
      fontFamily: fonts.prompt,
      fontSize : 20,
      textAlign: 'center'
    },
  
    bg: {
      position: 'absolute',
      left: 0,
      top: 0,
      right:0,
      bottom:0
    },
    walkthroughScrollView: {
      horizontal: true,
      snapeToAlignment: 'start'
    },
    carouselContainer : {
      paddingTop : 80,
      flex : 1,
    },
    carouselTitle: {
      fontsize : 20,
    },
    carouselItem : {
      width : '100%',
      height : screenWidth - 20,
    },
    carouselImageContainer : {
      flex : 1,
      borderRadius : 10,      
      backgroundColor : colors.background,
      height :100,
      marginBottom : Platform.select({ios: 0, android: 1})
    },
    carouselImage : {
      ...StyleSheet.absoluteFillObject,
      flex : 1,
      resizeMode : 'contain',
      width : screenWidth,
    },
    carouselDotContainer : {
      backgroundColor : '#EDCCAB',
      alignContent : 'center',
      justifyContent : 'center',
      flex : 1
    },
    carouselDotStyle : {
      width : 20,
      height : 20,
      borderRadius : 10,
      backgroundColor : '#1A1525',
    },
    carouselInactiveDotStyle : {
      backgroundColor : '#F8F8F8',
      borderColor : '#1A1525',
      borderWidth : 3
    }
  });
// Browser history back and forward button
/* Project specific Javascript goes here. */
const wrapper = document.querySelector(".wrapper"),
musicImg = wrapper.querySelector(".img-area img"),
musicName = wrapper.querySelector(".song-details .name"),
musicDefine = wrapper.querySelector(".song-details .artist"),
playPauseBtn = wrapper.querySelector(".play-pause"),
prevBtn = wrapper.querySelector("#prev"),
nextBtn = wrapper.querySelector("#next"),
mainAudio = wrapper.querySelector("#main-audio"),
progressArea = wrapper.querySelector(".progress-area"),
progressBar = progressArea.querySelector(".progress-bar"),
musicList = wrapper.querySelector("#playlist"),
radioKm = wrapper.querySelector("#radioKm"),
radioCountry = wrapper.querySelector("#radioC"),
radioOthers = wrapper.querySelector("#radioOthers"),
// moreMusicBtn = wrapper.querySelector("#moreMusic"),
// closemoreMusic = wrapper.querySelector("#close");

pauseSVG = "<path fill-rule='evenodd' d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z' clip-rule='evenodd'></path>";
playSVG = "<path fill-rule='evenodd' d='M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z' clip-rule='evenodd'></path>";

let musicIndex = Math.floor((Math.random() * sourceData.length) + 1);
// console.log(musicIndex)
// let musicIndex = sourceData[0].index;
isMusicPaused = true;
window.addEventListener("load", ()=>{
  loadMusic(musicIndex);
  playingSong(musicIndex);
});

function loadMusic(index){
  // if(sourceData[index])
  for(let t = 0; t < sourceData.length; t++) {
    if (sourceData[t].id == index) {
      console.log(sourceData[t].id)
      musicName.innerText = sourceData[t].radio_name;
      musicDefine.innerText = sourceData[t].radio_country;
      musicImg.src = sourceData[t].img;
      mainAudio.src = sourceData[t].uri;
    }
  }
};

//play music function
function playMusic(){
  wrapper.classList.add("paused");
  playPauseBtn.querySelector("svg").innerHTML = pauseSVG;
  playPauseBtn.classList.add("animate-spin")
  musicDefine.innerText = "Playing"
  musicDefine.classList.add("text-green-400")
  musicDefine.classList.remove("text-live-bg", "dark:text-primary")
  mainAudio.play();
};

//pause music function
function pauseMusic(){
  wrapper.classList.remove("paused");
  playPauseBtn.querySelector("svg").innerHTML = playSVG;
  musicDefine.innerText = "Paused"
  musicDefine.classList.remove("text-green-400")
  musicDefine.classList.add("text-live-bg", "dark:text-primary")
  mainAudio.pause();
};

//prev music function
function prevMusic(){
  musicIndex--; //decrement of musicIndex by 1
  //if musicIndex is less than 1 then musicIndex will be the array length so the last music play
  musicIndex < 1 ? musicIndex = sourceData.length : musicIndex = musicIndex;
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

//next music function
function nextMusic(){
  musicIndex++; //increment of musicIndex by 1
  //if musicIndex is greater than array length then musicIndex will be 1 so the first music play
  musicIndex > sourceData.length ? musicIndex = 1 : musicIndex = musicIndex;
  loadMusic(musicIndex);
  playMusic();
  playingSong(musicIndex);
};

// play or pause button event
playPauseBtn.addEventListener("click", ()=>{
  const isMusicPlay = wrapper.classList.contains("paused");
  //if isPlayMusic is true then call pauseMusic else call playMusic
  isMusicPlay ? pauseMusic() : playMusic();
  playingSong();
});

//prev music button event
prevBtn.addEventListener("click", ()=>{
  prevMusic();
});

//next music button event
nextBtn.addEventListener("click", ()=>{
  nextMusic();
});

// update progress bar width according to music current time
mainAudio.addEventListener("timeupdate", (e)=>{
  const currentTime = e.target.currentTime; //getting playing song currentTime
  const duration = e.target.duration; //getting playing song total duration
  let progressWidth = (currentTime / duration) * 100;
  progressBar.style.width = `${progressWidth}%`;

  let musicCurrentTime = wrapper.querySelector(".current-time"),
  musicDuartion = wrapper.querySelector(".max-duration");
  mainAudio.addEventListener("loadeddata", ()=>{
    // update song total duration
    let mainAdDuration = mainAudio.duration;
    let totalMin = Math.floor(mainAdDuration / 60);
    let totalSec = Math.floor(mainAdDuration % 60);
    if(totalSec < 10){ //if sec is less than 10 then add 0 before it
      totalSec = `0${totalSec}`;
    }
    musicDuartion.innerText = `${totalMin}:${totalSec}`;
  });
  // update playing song current time
  let currentMin = Math.floor(currentTime / 60);
  let currentSec = Math.floor(currentTime % 60);
  if(currentSec < 10){ //if sec is less than 10 then add 0 before it
    currentSec = `0${currentSec}`;
  }
  musicCurrentTime.innerText = `${currentMin}:${currentSec}`;
});

// update playing song currentTime on according to the progress bar width
progressArea.addEventListener("click", (e)=>{
  let progressWidth = progressArea.clientWidth; //getting width of progress bar
  let clickedOffsetX = e.offsetX; //getting offset x value
  let songDuration = mainAudio.duration; //getting song total duration

  mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
  playMusic(); //calling playMusic function
  // playingSong();
});


// let create li tags according to array length for list
// for (let i = 1; i <= sourceData.length; i++) {
//   //let's pass the song name, artist from the array
//   console.log(i);
//   let liAudioDuartionTag = musicList.querySelector(`#dur_${i}`);
//   let liAudioTag = musicList.querySelector(`.aud_${i}`);
//   liAudioTag.addEventListener("loadeddata", ()=>{
//     let duration = liAudioTag.duration;
//     let totalMin = Math.floor(duration / 60);
//     let totalSec = Math.floor(duration % 60);
//     if(totalSec < 10){ //if sec is less than 10 then add 0 before it
//       totalSec = `0${totalSec}`;
//     };
//     liAudioDuartionTag.innerText = `${totalMin}:${totalSec}`; //passing total duation of song
//     liAudioDuartionTag.setAttribute("t-duration", `${totalMin}:${totalSec}`); //adding t-duration attribute with total duration value
//   });
// };

//play particular song from the list onclick of li tag
function playingSong(trackIndex){
  if (musicList != null || musicList != undefined) {
    const Tracks = musicList.querySelectorAll("a .track");
    for (let j = 0; j < Tracks.length; j++) {
      console.log(Tracks.length)
      if(Tracks[j].getAttribute("li-index") != trackIndex){
        if(Tracks[j].classList.contains("playing")) {
          let audioTag = Tracks[j].querySelector(".audio-duration");
          Tracks[j].classList.remove("playing");
          audioTag.classList.remove("text-green-400", "animate:pulse")
          audioTag.innerText = sourceData[j].radio_country;
        }
        //audioTag.innerText = "Paused";
      }

      //if the li tag index is equal to the trackIndex then add playing class in it
      if(Tracks[j].getAttribute("li-index") === trackIndex){
        let audioTag = Tracks[j].querySelector(".audio-duration");
        Tracks[j].classList.add("playing");
        audioTag.classList.add("text-green-400", "animate:pulse")
        audioTag.innerText = "Playing";
      }

      Tracks[j].setAttribute("onclick", "clicked(this)");
    };
  }

  if (radioCountry != null || radioCountry != undefined) {
    const countryTracks = radioCountry.querySelectorAll("a .track");
    for (let j = 0; j < countryTracks.length; j++) {
      if(countryTracks[j].getAttribute("li-index") != trackIndex){
        if(countryTracks[j].classList.contains("playing")) {
          let audioTag = countryTracks[j].querySelector(".audio-duration");
          countryTracks[j].classList.remove("playing");
          audioTag.classList.remove("text-green-400", "animate:pulse")
          audioTag.innerText = sourceData[j].radio_country;
        }
        //audioTag.innerText = "Paused";
      }

      //if the li tag index is equal to the trackIndex then add playing class in it
      if(countryTracks[j].getAttribute("li-index") === trackIndex){
        let audioTag = countryTracks[j].querySelector(".audio-duration");
        countryTracks[j].classList.add("playing");
        audioTag.classList.add("text-green-400", "animate:pulse")
        audioTag.innerText = "Playing";
      }

      countryTracks[j].setAttribute("onclick", "clicked(this)");
    };
  }

  if (radioKm != null || radioKm != undefined) {
    const kmTracks = radioKm.querySelectorAll("a .track");

    for (let j = 0; j < kmTracks.length; j++) {
      if(kmTracks[j].getAttribute("li-index") != trackIndex){
        if(kmTracks[j].classList.contains("playing")) {
          let audioTag = kmTracks[j].querySelector(".audio-duration");
          kmTracks[j].classList.remove("playing");
          audioTag.classList.remove("text-green-400", "animate:pulse")
          audioTag.innerText = sourceData[j].radio_country;
        }
        //audioTag.innerText = "Paused";
      }

      //if the li tag index is equal to the trackIndex then add playing class in it
      if(kmTracks[j].getAttribute("li-index") === trackIndex){
        let audioTag = kmTracks[j].querySelector(".audio-duration");
        kmTracks[j].classList.add("playing");
        audioTag.classList.add("text-green-400", "animate:pulse")
        audioTag.innerText = "Playing";
      }

      kmTracks[j].setAttribute("onclick", "clicked(this)");
    };

  }

  if (radioOthers != null || radioOthers != undefined) {
    const otherTracks = radioOthers.querySelectorAll("a .track");

    for (let j = 0; j < otherTracks.length; j++) {
      if(otherTracks[j].getAttribute("li-index") != trackIndex){
        if(otherTracks[j].classList.contains("playing")) {
          let audioTag = otherTracks[j].querySelector(".audio-duration");
          otherTracks[j].classList.remove("playing");
          audioTag.classList.remove("text-green-400", "animate:pulse")
          audioTag.innerText = sourceData[j].radio_country;
        }
        //audioTag.innerText = "Paused";
      }

      //if the li tag index is equal to the trackIndex then add playing class in it
      if(otherTracks[j].getAttribute("li-index") === trackIndex){
        let audioTag = otherTracks[j].querySelector(".audio-duration");
        otherTracks[j].classList.add("playing");
        audioTag.classList.add("text-green-400", "animate:pulse")
        audioTag.innerText = "Playing";
      }

      otherTracks[j].setAttribute("onclick", "clicked(this)");
    }
  }
};


//particular li clicked function
function clicked(element){
  let getLiIndex = element.getAttribute("li-index");
  element.classList.add("playing")
  trackIndex = getLiIndex; //updating current song index with clicked li index
  if (element.classList.contains("playing")) {
    loadMusic(trackIndex);
    playMusic();
    playingSong(trackIndex);
    // element.querySelector(".audio-duration").classList.add("text-green-400")
    // element.querySelector(".audio-duration").innerHTML = "Playing"
  } else {
    pauseMusic();
    // element.querySelector(".audio-duration").classList.remove("text-green-400")
    // element.querySelector(".audio-duration").innerHTML = "0.00"
  }
};

function mapPlay(element){
  let getIndex = element.getAttribute("data-index");
  radioIndex = getIndex; //updating current song index with clicked li index
  playMusic();
  loadMusic(radioIndex);
  playingSong(radioIndex);
};

function tapped(element){
  let getIndex = element.getAttribute("data-index");
  element.classList.toggle("playing")
  radioIndex = getIndex; //updating current song index with clicked li index
  if (element.classList.contains("playing")) {
    loadMusic(radioIndex);
    playMusic();
    playingSong(radioIndex);
    // element.classList.add("animate-pulse")
    // element.innerHTML = pauseSVG;
  } else {
    pauseMusic();
    // element.classList.remove("animate-pulse")
    // element.innerHTML = playSVG;
  }
};







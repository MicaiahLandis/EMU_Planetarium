// Laura Benner
// laurabennerr@gmail.com
// EMU Engineering Capstone 2024-25

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('nav ul li');
    const contents = document.querySelectorAll('.tab-content');

    // Switch between tabs
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(content => content.classList.remove('active'));
            tab.classList.add('active');
            const contentId = tab.id.replace('-tab', '');
            document.getElementById(contentId).classList.add('active');
        });
    });

    // Send request to backend
    function postRequest(url, data) {
        console.log("requested")
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .catch(error => console.error("Error:", error));
    }

    // Update motion based on inputs from Continuous Motion page
    document.querySelectorAll('.motion-box').forEach((box, index) => {
        const checkbox = box.querySelector('.axis-checkbox');
        const speedSelect = box.querySelector('select[id$="-speed"]');
        const directionSelect = box.querySelector('select[id$="-direction"]');
    
        function updateMotion() {
            const axis = index + 1;
            const direction = directionSelect.value;
            const speed = speedSelect.value;
            const extra = checkbox.checked;
    
            postRequest('/update_motion', { axis, direction, speed, extra })
                .catch(error => console.error("Error:", error));
        }
    
        checkbox.addEventListener('change', updateMotion);
        speedSelect.addEventListener('change', updateMotion);
        directionSelect.addEventListener('change', updateMotion);
    });
    
    // Update motion based on inputs from Sky Simulator page
    document.getElementById('sky-simulator-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const latitude = parseFloat(document.getElementById('latitude').value);
        const longitude = parseFloat(document.getElementById('longitude').value);
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
    
        if (latitude < -90 || latitude > 90) {
            alert('Please enter a valid latitude between -90 and 90 degrees.');
            return;
        }
    
        if (longitude < -180 || longitude > 180) {
            alert('Please enter a valid longitude between -180 and 180 degrees.');
            return;
        }
    
        postRequest('/sky_simulator', { latitude, longitude, date, time })
            .then(data => console.log("Moving to sidereal time:", data))
            .catch(error => console.error("Error:", error));
    });

    // Calibrate
    document.getElementById('calibrate-button').addEventListener('click', function () {
        const overlay = document.getElementById('overlay');
        overlay.style.display = 'flex';
        postRequest('/calibrate', {})
        .then(data => {
            overlay.style.display = 'none';
            console.log("Calibration started:", data);
        })
        .catch(error => {
            overlay.style.display = 'none';
            console.error("Error:", error);
        });
    });

    // Lights and their associated pins
    const checkboxes = [
        { id: 'star-checkbox', pins: [26] },
        { id: 'ecliptic-checkbox', pins: [19] },
        { id: 'meridian-checkbox', pins: [12] },
        { id: 'equatorial-checkbox', pins: [13] },
        { id: 'geo-earth-checkbox', pins: [16] },
        { id: 'pole-light-checkbox', pins: [24] },
        { id: 'twilight-checkbox', pins: [5, 6] },
        { id: 'cardinal-points-checkbox', pins: [7] },
        { id: 'latitude-checkbox', pins: [17] },
        { id: 'moon-checkbox', pins: [18] },
        { id: 'sun-checkbox', pins: [27] },
        { id: 'planets-checkbox', pins: [22, 23] },
        { id: 'orion-checkbox', pins: [3] },
        { id: 'cassiopeia-checkbox', pins: [2] }
    ];
    
    // Turn lights on/off
    checkboxes.forEach(({ id, pins }) => {
        const checkbox = document.getElementById(id);
        checkbox.addEventListener('change', () => {
            postRequest('/toggle-light', { pins })
                .then(data => console.log("Light toggled:", data.light))
                .catch(error => console.error(error));
        });
    });

    // "Stars for a Night in Spring" script
    const script = [
        ["Click Next to Start the Show"],
        ["Welcome to our program entitled “Stars for a Night in Spring!” We are going to be spinning some yarns and telling legends about some of the interesting constellations which we can see from Harrisonburg at this time of the year, during the month of April."],
        ["First of all let's take a look at the sky around sunset, about half past eight o'clock in the evening. Over towards the southwest you see the star Sirius, sometimes called the Dog Star. The star Sirius along with Procyon and Betelgeuse form the beautiful Winter Triangle. Betelgeuse is in the shoulder of the constellation of Orion the Hunter."],
        ["Orion the Hunter is down on our western horizon and will set very soon after the sun, so if you want to see the constellation you will have to look for it in the west, shortly after sunset. You can see the belt of Orion there and the shield pointing towards the constellation of Taurus the Bull just charging up above the western horizon. The star Sirius is in the constellation of Canis Major, the Great Dog, one of the hunting dogs of Orion. Here you see his head, and his body, and his legs. And over here a little higher you see the little hunting dog, Canis Minor with the bright star Procyon."],
        ["One of the most spectacular objects in the sky is the constellation of Leo the Lion. It's almost directly overhead at sunset at this time of the year. We see the bright star Regulus in the shoulder of Leo and the sickle shaped group of stars forms the head of the lion, and here we see the body and the tail, with the star Denebola at the end of the tail. Let's move toward the North."],
        ["Here in the North we see another very bright and important constellation,  almost directly overhead: the Big Dipper. There we see the handle of the dipper and here is the bowl. The Big Dipper is actually part of a much larger constellation known as the Great Bear or Ursa Major. Right behind the bear you see a large serpentine form in the sky: Draco the Dragon. The dragon wraps down almost to the northern horizon where we can maybe pick out the dim stars that make up his head. The star Polaris, at the end of the handle of the Little Dipper, is our North Star in this epoch."],
        ["As the Earth moves through its 24 hours of rotation, Polaris stays approximately stationary along the meridian line, which divides the sky into its Eastern and Western hemispheres. The bright lights which you see surrounding the perimeter of the planetarium of course represent the city lights of Harrisonburg. The light pollution dims out all of the stars on the horizon. Let's take our journey back to the year 3000 B. C. where the city lights of Harrisonburg will of course no longer be visible. The sky will be much more brilliant and we will be able to observe some of the constellation shapes more clearly."],
        ["Look now towards the west. Here we see the twin stars Castor and Pollux in the constellation Gemini. There are many interesting legends associated with this particular group of stars. Probably the most famous is Jason in his pursuit of the Golden Fleece. He had the twin boys Castor and Pollux along in a ship with him. A tremendous storm arose and finally subsided when lights appeared shining on the foreheads of the twins. So from then on they believed that the twin stars were a good sailing omen. In fact, sometimes they are also used as a weather sign, if you can only see one star, unsettled weather lies ahead but if you can see both stars then fair weather lies ahead. If you will remember in the book of Acts, the Apostle Paul mentions on his journey to Rome that he sailed on the ship which carried the insignia of Castor and Pollux. The poet Macaulay expresses it in this fashion:",
        "",
        "\"Safe comes the ship to heaven",
        "Through billows and through gales",
        "If once the great Twin Brethren",
        "Set shining on the sails.\"",
        "",
        "Astrology also speaks of the twin stars, Castor and Pollux. Castor represents the Object of mind and Pollux the subject of mind. The object of mind deals with reason but subject of mind deals with intuition. Astrology says that if both reason and intuition are in equal balance then smooth sailing is predicted for human voyage, however if reason overshadows intuition or vice versa then rough sailing in the human voyage lies ahead."],
        ["There are twelve constellations which lie along the ecliptic line which is the path the sun appears to travel in the sky. These are called the Constellations of the Zodiac. Astrologers attach great significance to these constellations. Of course, most scientists have no faith whatsoever in this type of teaching. One rather interesting note here is that in the year 3000 B.C. when the Sun entered the constellation of Leo, it was highest above the celestial equator. This means that the sun enters the constellation of Leo on the hottest and longest days of the year. Now why do we refer to this constellation as the lion? Perhaps one interesting suggestion is this: The sun of course is the ruler of the heavenly bodies as far as we are concerned here on the earth, and the lion is the ruler of beasts. Many of the ancients used to think of the sun as residing in the constellation of the lion. The Greek poet Aratus refers to this when he says:",
        "",
        "\"The Lion flames. There the Sun's course runs hottest.",
        "Empty of grain the arid fields appear",
        "When first the Sun into the Lion enters.\""],
        ["Moving next along the ecliptic we come to Virgo, sometimes called the goddess of justice. There's one bright star in the constellation of Virgo  called Spica. You can find the star Spica by first locating the big dipper and tracing the handle down to the bright star Arcturus in the constellation of Bootes and then if you arch on around we come to the star, Spica, a very beautiful star in the May sky. Legend has it that in ancient prehistoric time, during the time of the Garden of Eden in other cultures, Virgo was the goddess of justice and presided over humankind. Humankind was at peace among himself and also with nature and Virgo enjoyed her task very much. However man became more arrogant and self destructive and finally Virgo could stand it no longer and winged her flight into the heavens. The poet Aratus refers to this when he says:",
        "",
        "\"But when that generation died, and there was born",
        "A brazen generation, more pernicious than their sires,",
        "Who forged the felon sword",
        "For hostile foray, and tasted the blood of the ox that drew the plough,",
        "Justice, loathing that race of men,",
        "Winged her flight to heaven; and fixed her station in that region",
        "Where still by night is seen",
        "The Virgin goddess, near to bright Bootes.\"",
        "",
        "At times, the virgin is also referred to as the goddess of harvest. She is sometimes pictured as holding a sheath of grain in her hand. This is because the sun entered the constellation of Virgo in the early harvest season."],
        ["Next we move across the sky to the constellation of Bootes the Ploughman. There's a very bright star in this constellation, the star Arcturus. It's sometimes referred to as Job's star because it's mentioned in the Book of Job. Arcturus lies in the girdle of Bootes the Ploughman. Here we see the legs of the ploughman, here's his body, and here's his head. He's usually referred to as pulling or pushing a large wagon in the sky which is the Big Dipper! The handle of the dipper could refer to the tongs of the wagon, and the bowl is sort of the body of the wagon. Once you find Bootes, one can easily locate the Northern Crown, a beautiful crescent shaped group of stars in this region of the sky."],
        ["Moving toward the North, I'd like to point out to you that the star Polaris has drifted considerably from the north axis on our celestial sphere. Moving back 5000 years at the beginning of the program demonstrated the precessional effect, which is the gradual rotation of Earth's axis over a cycle of 26,000 years."],
        ["We come now to one of the most spectacular objects of the sky, and that is the Big Dipper. Let me point the constellation Ursa Major out to you again. Here you see the long tail, the bowl of the dipper forming the body of the bear, there are the hind legs, the front legs and the head of the bear. Now if you know anything about bears you know that they have short tails but our great bear in the sky has a very long tail. How did the bear get such a long tail? Well there is a legend associated with this particular constellation. It is supposed that the god Jupiter was angry with one of the subjects and turned him into a bear, and he placed him into the forest. One day Jupiter, surveying the situation, found a hunter entering the forest and he didn't want the bear to be killed so he snatched the bear out of the woods by the tail, and flung him into the sky and so we have the great bear in the sky. In the process of carrying the bear by the tail and flinging him into the sky the bear's tail was stretched and that's how we have the legend of the great bear with the long tail in the sky. Well, perhaps this a rather long tail but the Roman poet, Ovid writes:",
        "",
        "\"Snatched them through the air",
        "In whirlwinds up to heaven and fixed them there;",
        "Where the new constellations nightly rise,",
        "And add a lustre to the northern skies.\"",
        "",
        "Well, perhaps we should head for shelter to avoid this thunderstorm. I hope you have enjoyed our program this evening and our visit with the \"Stars for a Night in Spring.\""]
    ];
    
    let currentIndex = 0;

    const textElement = document.getElementById('text');
    const counterElement = document.getElementById('counter');
    const nextButton = document.getElementById('next');
    
    // Update script content and counter
    function updateContent() {
        textElement.innerHTML = script[currentIndex].join("<br>");
        counterElement.textContent = `${currentIndex + 1}/${script.length}`;
        if (currentIndex === script.length - 1) {
            nextButton.textContent = "Finish";
        } else {
            nextButton.textContent = "Next";
        }
    }
    
    // Update script content and trigger projector motions/lights when next is clicked
    nextButton.addEventListener('click', () => {
        currentIndex++;
        fetch(`/show/${currentIndex}`, {
            method: 'POST',
        }).then(response => {
            if (!response.ok) {
                console.error('Slide update');
            }
        }).catch(error => {
            console.error('Error going to slide', error);
        });
        if (currentIndex === script.length) {
            currentIndex = 0;
        }
        updateContent();
    });
    
    updateContent();

});

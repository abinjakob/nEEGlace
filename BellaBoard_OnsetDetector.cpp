/**
Audio onset detection using energy of the signal
-----------------------------------------------
The script reads audio samples (currently only from one input) into a buffer and 
for every hopSize it calculates the energy of the buffer. If energy is higher than
the energyThreshold it activates the digital pin if it is not in the refractory period 
*/

#include <Bela.h>
#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

// config file 
const std::string configFilename = "config.txt"; 

// configuration parameters
int bufferSize = 512; 						// num of samples stored in buffer for energy calculation
int hopSize = 256;			 				// interval at which buffer is processed
float refractoryPeriod = 0.5;				// refractory period (sec)
float activationDuration = 0.05;			// duration to activate the digital output pin after onset detection (sec)
int inputGain = 55;							// input gain for the microphones 	
float energyThreshold = 0.2;				// threshold for detecting an onset
float toneFreq = 200.0;

// state variables
std::vector<float> audioBuffer(bufferSize, 0.0f);
int bufferIndex = 0;						// current position in audioBuffer
int hopCounter = 0;							// to track samples processed since last energy calculation 
int refractoryPeriodSamples;
int refractoryCounter = 0;					// to track refractory period
int timeSinceLastOnset = 0; 				// to track samples since last onset
int activationDurationSamples;
int activationCounter = 0;					// to track how long digital output is activated
const int digitalPin = 0;					// digital pin number to activate

// function to read from config file 
bool readConfig(const std::string& filename){
	// opening config file 
	std::ifstream configFile(filename);
	// throw error if config file cannot be opened 
	if(!configFile.is_open()){
		rt_printf("Cannot open the config file");
		return false;
	}
	
	std::string line;
	// reading each line in the config file 
	while(std::getline(configFile, line)){
		std::istringstream iss(line);
		std::string key;
		// looking for energy threshold key in config 
		if(iss >> key && key == "energyThreshold"){
			// read and parse energy threshold value
			if(!(iss >> energyThreshold)){
				rt_printf("Error reading energy threshold value\n");
				return false;
			}
		}
	}
	
	// closing config file
	configFile.close();
	return true;
}

// function to calculate energy of a buffer
float calculateEnergy(const std::vector<float>& buffer) {
	float energy = 0.0f;
	for (const auto& sample : buffer) {
		energy += sample * sample;
	}
	return energy / buffer.size();
}

// function to setup
bool setup(BelaContext *context, void *userData) {
	// setting input gain for left and right
	Bela_setAudioInputGain(0, inputGain);			
	Bela_setAudioInputGain(1, inputGain);
	
	// converting to samples
	refractoryPeriodSamples = context->audioSampleRate * refractoryPeriod;
	activationDurationSamples = context->audioSampleRate * activationDuration;
	
	// seting digital pin as output pin
	pinMode(context, 0, digitalPin, OUTPUT);   
	
	// read config file 
	if(!readConfig(configFilename)){
		rt_printf("Using default energy threshold value: %f\n", energyThreshold);
	} else {
		rt_printf("Using energy threshold value from config file: %f\n", energyThreshold);
	}
	
	return true;
}

// function to render new audio samples
void render(BelaContext *context, void *userData) {
	static float phase = 0.0f;
	float phaseIncrement = 2.0f * M_PI * toneFreq / context->audioSampleRate;
	
	// loop over each sample
	for (unsigned int n = 0; n < context->audioFrames; ++n) {
		// read the current sample from the input channel 0
		float currentSample = audioRead(context, n, 0);
	    // update the buffer with the current sample
	    audioBuffer[bufferIndex] = currentSample;
	    bufferIndex = (bufferIndex + 1) % bufferSize;
	
	    // increment hop counter
	    hopCounter++;
	    // wainitng until hopSize is reached  
	    if (hopCounter >= hopSize) {
	    	// reset hopCounter
	        hopCounter = 0;
	
	        // calculate energy
	        float energy = calculateEnergy(audioBuffer);
	        // Print the energy value to the command line
	        //rt_printf("Energy: %f\n", energy);
	
	        // check for energy-based onset detection
	        if (energy >= energyThreshold && refractoryCounter <= 0) {
	            rt_printf("Onset detected! Energy: %f\n", energy);
	            rt_printf("Time since last onset: %f seconds\n", timeSinceLastOnset / context->audioSampleRate);
	
	            refractoryCounter = refractoryPeriodSamples;		 // set the refractory counter
	            timeSinceLastOnset = 0;								 // reset the counter for time since last onset
	            activationCounter = activationDurationSamples;       // set the activation counter
	            digitalWrite(context, n, digitalPin, HIGH);          // activate the digital output pin
	            // rt_printf("Pin On\n");
	            
	            //audioWrite(context, n, 0, out);
	            //audioWrite(context, n, 1, out);
	            
	        }
	    }
	    
	    // decrement the refractory counter if it's active
	    if (refractoryCounter > 0) {
	        refractoryCounter--;
	    }
	    
	    // increment the counter for time since last onset
	    timeSinceLastOnset++;
	    
	    // handle the digital output activation duration
	    if (activationCounter > 0) {
	        activationCounter--;
	        if (activationCounter == 0) {
	            digitalWrite(context, n, digitalPin, LOW);			  // deactivate the digital output pin
	            // rt_printf("Pin Off\n");
	            
	            //audioWrite(context, n, 0, out);
	        	//audioWrite(context, n, 1, out);
	        }
	        
	        // send audio pulse to audio output pin when trigger detected
	        float out = sinf(phase);
	        phase += phaseIncrement;
	        if(phase >= 2.0f * M_PI){
	        	phase -= 2.0f * M_PI;
	        }
	        audioWrite(context, n, 0, out);
	        audioWrite(context, n, 1, out);
		} else {
			audioWrite(context, n, 0, 0.0f);
	        audioWrite(context, n, 1, 0.0f);
		}
	}
}

void cleanup(BelaContext *context, void *userData) {}

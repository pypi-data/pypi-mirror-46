# Gaussian and Binomial Distributions

This package allows the user to easily get the main statistics, plot the distributions and add up two Gaussians or two Binomial distributions.

## Table of Contents
* [Installation](#Installation)
* [File Description](#description)
* [Licensing, Authors, Acknowledgements](#licensing)

## Installation
The code requires Python versions of 3.*.

## File Description <a name="description"></a>
class Gaussian(data)

Parameters:
	data : list of samples
    
Methods:
	calculate_mean(self) : Function to calculate the mean of the data set.
        Returns: mean of the distribution
	calulcate_stdev(self) : Function to calculate the standard deviation of the data set.
        Returns: standard deviation of the distribution
	plot_histogram(self) : Function to output a histogram of the instance variable data using matplotlib pyplot library.
        Returns: histogram of distribution
	pdf(self, x) : Probability density function calculator for the gaussian distribution.
    	Parameters: x (float): point for calculating the probability density function
    	Returns: Float: probability density function output
	plot_histogram_pdf(self, n_spaces = 50) : Function to plot the normalized histogram of the data and a plot of the probability density function along the same range n_spaces
    	Parameters: n_spaces (int): number of data points 
        Returns: 
        	list: x values for the pdf plot
			list: y values for the pdf plot
	__add__(self, other) : Function to add together two Gaussian distributions
    	Parameters: other (Gaussian): Gaussian instance
        Returns: Gaussian: Gaussian distribution
	__repr__(self) : Function to output the characteristics of the Gaussian instance
    	Returns: string: characteristics of the Gaussian

class Binomial(data)

Parameters:
	data : list of samples
    
Methods: 
	calculate_mean(self) : Function to calculate the mean from p and n
    	Returns: float: mean of the data set
	calulcate_stdev(self) : Function to calculate the standard deviation from p and n.
    	Returns: float: standard deviation of the data set
	replace_stats_with_data(self) : Function to calculate p and n from the data set
    	Returns: 
        	float: the p value
            float: the n value
	plot_bar(self) : Function to output a histogram of the instance variable data using matplotlib pyplot library.
	pdf(self, k) : Probability density function calculator for the gaussian distribution.
    	Parameters: x (float): point for calculating the probability density function
        Returns: Float: probability density function output
	plot_bar_pdf(self) : Function to plot the pdf of the binomial distribution
    	Returns: 
        	list: x values for the pdf plot
            list: y values for the pdf plot
	__add__(self, other) : Function to add together two Binomial distributions with equal p
    	Parameters: other (Binomial): Binomial instance
        Returns: Binomial: Binomial distribution
	__repr__(self) : Function to output the characteristics of the Binomial instance
    	Returns: string: characteristics of the Gaussian

## Licensing, Authors, Acknowledgements <a name="licensing"></a>
Licensing information can be looked up from the license.txt file.

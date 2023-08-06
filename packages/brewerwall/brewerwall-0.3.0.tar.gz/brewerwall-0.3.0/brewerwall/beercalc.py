# -*- coding: utf-8 -*-

"""Main module."""

from math import pow, e


def abv(originalGravity: float, finalGravity: float) -> float:
    """
    Determines the Alochol by Volume (ABV).

    Parameters
    ----------
    originalGravity : float
        Original gravity of wort.
    finalGravity : float
        Final gravity of beer.
    
    Returns
    -------
    float or None
        Alcohol by Volume.
    """

    if originalGravity > finalGravity:
        return (
            76.08 * (originalGravity - finalGravity) / (1.775 - originalGravity)
        ) * (finalGravity / 0.794)
    else:
        return


def abw(originalGravity: float, finalGravity: float) -> float:
    """
    Determines Alochol by Weight (ABW).

    Parameters
    ----------
    originalGravity : float
        Original gravity of wort.
    finalGravity : float
        Final gravity of beer.
    
    Returns
    -------
    float or None
        Alcohol by Weight.
    """

    if originalGravity > finalGravity:
        return (0.79 * abv(originalGravity, finalGravity)) / finalGravity
    else:
        return


def mcu(pounds: float, lovibond: float, gallons: float) -> float:
    """
    Determines Malt Color Unit (MCU).

    Parameters
    ----------
    pounds : float
        Weight in pounds.
    lovibond : float
        Color of malt in degrees lovibond.
    gallons : float
        Water volume in gallons.

    Returns
    -------
    float or None
        Malt Color Unit.
    """

    if gallons != 0:
        return (pounds * lovibond) / gallons
    else:
        return


def srm(pounds: float, lovibond: float, gallons: float) -> float:
    """
    Determines Standard Reference Method (SRM).

    Parameters
    ----------
    pounds : float
        Weight in pounds.
    lovibond : float
        Color of malt in degrees lovibond.
    gallons : float
        Water volume in gallons.

    Returns
    -------
    float or None
        Standard Reference Method.
    """

    if gallons != 0:
        return 1.4922 * (pow(mcu(pounds, lovibond, gallons), 0.6859))
    else:
        return


def aau(alphaAcid: float, ounces: float) -> float:
    """
    Determines Alpha Acid Unit.

    Parameters
    ----------
    alphaAcid : float
        Alpha acid percentage.
    ounces : float
        Weight in ounces.
    
    Returns
    -------
    float or None
        Alpha Acid Unit.
    """

    if (alphaAcid and ounces) > 0:
        return alphaAcid * ounces
    else:
        return


def utilization(minutes: float, specificGravity: float) -> float:
    """
    Determines Hop Utilization.

    Parameters
    ----------
    minutes : float
        Time in minutes.
    specificGravity : float
        Specific gravity.
    
    Returns
    -------
    float
        Hop Utilization.
    """

    return (
        (1.65 * pow(0.000125, (specificGravity - 1)))
        * (1 - pow(e, (-0.04 * minutes)))
        / 4.15
    )


def ibu(
    alphaAcid: float,
    ounces: float,
    minutes: float,
    specificGravity: float,
    gallons: float,
) -> float:
    """
    Determines International Bitterness Units (IBU).

    Parameters
    ----------
    alphaAcid : float
        Alpha acid percentage.
    ounces : float
        Weight in ounces.
    minutes : float
        Time in minutes.
    specificGravity : float
        Specific gravity.
    gallons : float
        Water volume in gallons.

    Returns
    -------
    float or None
        International Bitterness Units.
    """

    if gallons != 0:
        return (
            aau(alphaAcid, ounces)
            * utilization(minutes, specificGravity)
            * 75
            / gallons
        )
    else:
        return


def convertToPlato(specificGravity: float) -> float:
    """
    Convert Specific Gravity to Plato.

    http://hbd.org/ensmingr/

    Parameters
    ----------
    specificGravity : float
        Specific gravity.
    
    Returns
    -------
    float
        Degress plato.
    """

    return (-463.37) + (668.72 * specificGravity) - (205.35 * pow(specificGravity, 2))


def realExtract(originalGravity: float, finalGravity: float) -> float:
    """
    Determine the Real Extract value of wort.

    http://hbd.org/ensmingr/

    Parameters
    ----------
    originalGravity : float
        Original gravity of wort.
    finalGravity : float
        Final gravity of beer.
    
    Returns
    -------
    float or None
        Real extract value.
    """

    if originalGravity > finalGravity:
        return (0.1808 * convertToPlato(originalGravity)) + (
            0.8192 * convertToPlato(finalGravity)
        )
    else:
        return


def calories(originalGravity: float, finalGravity: float) -> float:
    """
    Determine Calories per 12oz Serving.
    
    Parameters
    ----------
    originalGravity : float
        Original gravity of wort.
    finalGravity : float
        Final gravity of beer.
    
    Returns
    -------
    float or None
        Calories.
    """

    if originalGravity > finalGravity:
        return (
            (
                (6.9 * abw(originalGravity, finalGravity))
                + 4.0 * (realExtract(originalGravity, finalGravity) - 0.1)
            )
            * finalGravity
            * 3.55
        )
    else:
        return


def attenuation(originalGravity: float, finalGravity: float) -> float:
    """
    Determines Attenuation of yeast.

    Parameters
    ----------
    originalGravity : float
        Original gravity of wort.
    finalGravity : float
        Final gravity of beer.
    
    Returns
    -------
    float or None
        Attenuation.
    """

    if originalGravity > finalGravity:
        return (originalGravity - finalGravity) / (originalGravity - 1)
    else:
        return


def gravityCorrection(
    fahrenheit: float, specificGravity: float, calibrationFahrenheit: float
) -> float:
    """
    Determines Gravity Temperature Correction.

    Parameters
    ----------
    fahrenheit : float
        Temperature in fahrenheit.
    specificGravity : float
        Specific gravity.
    calibrationFahrenheit : float
        Calibration temperature in fahrenheit
    
    Returns
    -------
    float
        Gravity temperature correction.
    """

    return specificGravity * (
        (
            1.00130346
            - 0.000134722124 * fahrenheit
            + 0.00000204052596 * pow(fahrenheit, 2)
            - 0.00000000232820948 * pow(fahrenheit, 3)
        )
        / (
            1.00130346
            - 0.000134722124 * calibrationFahrenheit
            + 0.00000204052596 * pow(calibrationFahrenheit, 2)
            - 0.00000000232820948 * pow(calibrationFahrenheit, 3)
        )
    )


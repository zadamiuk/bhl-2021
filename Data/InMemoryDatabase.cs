using System;
using System.Collections.Generic;
using System.Text;
using BHL_cieplo.Models;

namespace BHL_cieplo.Data
{
    static class InMemoryDatabase
    {
        static List<PhotovoltaicCellPerformanceDetails> photovoltaicCellPerformanceDetailsList = new List<PhotovoltaicCellPerformanceDetails>() {
            new PhotovoltaicCellPerformanceDetails(new List<int>(){1,12}, new List<TimePeriod>(){new TimePeriod(15,8)}, 0, 90, 100),
            new PhotovoltaicCellPerformanceDetails(new List<int>(){1,12}, new List<TimePeriod>(){new TimePeriod(8,10)}, 1.5, 90, 100)
        };
  
    }
}

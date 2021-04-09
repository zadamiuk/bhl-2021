using System;
using System.Collections.Generic;
using System.Text;

namespace BHL_cieplo.Models
{
    public class PhotovoltaicCellPerformanceDetails
    {
        public List<Month> Months { get; set; }
        public List<TimePeriod> Periods { get; set; }
        public int PowerProduced { get; set; }
        public int BottomCloudPercentage { get; set; }
        public int TopCloudPercentage { get; set; }
    }
}

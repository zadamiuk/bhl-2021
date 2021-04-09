using System;
using System.Collections.Generic;
using System.Text;

namespace BHL_cieplo.Models
{
    class PriceList
    {
        public Month Month { get; set; }
        public TypeOfDay TypeOfDay { get; set; }
        public TimePeriod TimePeriod { get; set; }
        public float PowerBuyPrice { get; set; }
        public float PowerSellPrice { get; set; }
    }
}

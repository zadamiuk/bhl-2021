using System;

namespace BHL_cieplo.Models
{
    public class TimePeriod
    {
        public int StartTime { get; set; }
        public int EndTime { get; set; }

        public TimePeriod(int startTime, int endTime)
        {
            StartTime = startTime;
            EndTime = endTime;
        }
    }
}
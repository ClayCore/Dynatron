using System;
using System.IO;
using WebWindows;

namespace Dynatron.Core {
    internal class Program {
        private static readonly string m_EntryPoint = "./Web/build/debug/index.html";
        static void Main(string[] args) {
            if (File.Exists(m_EntryPoint)) {
                Console.WriteLine("[INFO/Thread]: File exists!");

                WebWindow m_Window = new WebWindow("Dynatron Server");
                m_Window.NavigateToLocalFile(m_EntryPoint);
                m_Window.Show();
                m_Window.WaitForExit();
            }
        }
    }
}

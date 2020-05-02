using System;
using System.IO;
using System.Diagnostics;
using SpiderEye;
using SpiderEye.Windows;

namespace Dynatron.Core {
    public abstract class ProgramBase {
        protected static void Run() {
            using (var window = new Window()) {
                Application.ContentProvider = new EmbeddedContentProvider("Client\\build\\debug\\");

                window.EnableDevTools = true;

                Application.Run(window, "index.html");
            }
        }
    }

    internal class Program : ProgramBase {

        [STAThread]
        static void Main(string[] args) {
            WindowsApplication.Init();
            Run();
        }
    }
}
